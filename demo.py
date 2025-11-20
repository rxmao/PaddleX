#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF / DOC / DOCX → Markdown / JSON / 图片
MetaX GPU 适配版本
----------------------------------------
✓ 支持MetaX GPU和NVIDIA GPU设备
✓ doc/docx 自动转 PDF（使用WPS在线转换服务，可选）
✓ 每页生成 page_xxx/{page.md,page.json,images/…}
✓ 合并生成 merged.md，保留页眉/页脚/页号信息
✓ 输出 imgs/ 统一图片目录
✓ 返回 (out_dir, pages_list, time_stats) 供 API 调用
✓ 支持外部传入 pipeline 实例以复用模型
"""

import sys
sys.setrecursionlimit(10000)  # 防止 markdownify 嵌套过深

import json, re, textwrap, shutil, tempfile, time
from pathlib import Path
from typing import Union, List, Tuple, Optional, Dict

from paddlex import create_pipeline
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# WPS转换器 - 可选功能
try:
    from wps_word2pdf import WordToPdfConverter
    HAS_WPS_CONVERTER = True
except ImportError:
    HAS_WPS_CONVERTER = False
    print("⚠️  未安装wps_word2pdf，Word转PDF功能不可用")


# ========== 设备配置 ==========
def detect_device():
    """自动检测可用设备"""
    try:
        import paddle
        custom_devices = paddle.device.get_all_custom_device_type()
        if 'metax_gpu' in custom_devices:
            return 'metax_gpu:0'
        elif paddle.device.is_compiled_with_cuda():
            return 'gpu:0'
        else:
            return 'cpu'
    except Exception as e:
        print(f"⚠️  设备检测失败: {e}，使用CPU")
        return 'cpu'


DEFAULT_DEVICE = detect_device()


# ---------- DOC/DOCX → PDF --------------------------------------------------
def _doc_to_pdf(src: Path, out_dir: Path) -> Tuple[Path, float]:
    """
    使用WPS在线服务将doc/docx转换为PDF
    返回: (PDF路径, 转换耗时毫秒)
    """
    if not HAS_WPS_CONVERTER:
        raise RuntimeError(
            "Word转PDF功能需要安装wps_word2pdf模块\n"
            "请运行: pip install wps_word2pdf"
        )
    
    out_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = out_dir / (src.stem + ".pdf")

    # 创建转换器实例
    converter = WordToPdfConverter()

    # 记录开始时间
    start_time = time.perf_counter()

    # 执行转换
    success = converter.convert(
        input_path=str(src),
        output_path=str(output_pdf),
        verbose=False
    )

    # 计算耗时
    conversion_time = (time.perf_counter() - start_time) * 1000

    if not success:
        raise RuntimeError(f"Word文档转换PDF失败: {src}")

    return output_pdf, conversion_time


# ---------- 图片钩子 ---------------------------------------------------------

def process_image(pg_idx: int, local_path: Path, global_img_dir: Path) -> Union[str, None]:
    """复制图片到全局图片目录"""
    dest = global_img_dir / local_path.name
    shutil.copyfile(local_path, dest)
    return None  # 保持相对路径 imgs/xxx


# ---------- HTML → Markdown -------------------------------------------------

def _extract_tables(soup: BeautifulSoup):
    """
    将 <table> 元素替换为占位符并提取为 Markdown。
    """
    phs, tables = [], []
    for i, tbl in enumerate(soup.find_all("table")):
        # 预检查：跳过没有实际内容的表格
        if not tbl.find_all(['tr', 'td', 'th']):
            continue

        html = str(tbl)
        try:
            dfs = pd.read_html(html, flavor="bs4")
        except (ValueError, IndexError, KeyError, AttributeError, Exception) as e:
            print(f"⚠️  跳过无法解析的表格 {i}: {type(e).__name__}")
            continue

        if not dfs:
            continue

        try:
            df = dfs[0]
            if df.empty:
                continue
            tables.append(df.to_markdown(index=False))
            ph = f"<<TABLE{i}>>"
            phs.append(ph)
            tbl.replace_with(ph)
        except Exception as e:
            print(f"⚠️  无法转换表格 {i} 为 Markdown: {type(e).__name__}")
            continue

    return phs, tables


def html_fragment_to_md(html: str) -> str:
    """将 HTML 片段转换为 Markdown 格式"""
    try:
        soup = BeautifulSoup(html, "lxml")
        phs, tables = _extract_tables(soup)
        body = md(str(soup), strip=["html", "body", "div"])
        for ph, t in zip(phs, tables):
            body = body.replace(ph, "\n" + t + "\n")
        body = textwrap.dedent(body).strip()
        return re.sub(r"\n{3,}", "\n\n", body)
    except RecursionError:
        print("⚠️  HTML → Markdown 递归过深，返回原始内容")
        return html
    except Exception as e:
        print(f"⚠️  HTML → Markdown 转换失败: {type(e).__name__}，返回原始内容")
        return html


def fix_image_path(text: str, pg_idx: int) -> str:
    """修正图片路径"""
    pre = f"page_{pg_idx:03d}/"
    text = re.sub(r'!\[(.*?)\]\(\s*images/([^)\s]+)\)', fr'![\1]({pre}images/\2)', text, flags=re.I)
    text = re.sub(r'src=["\']\s*images/([^"\']+)["\']', fr'src="{pre}images/\1"', text, flags=re.I)
    return text


# ---------- 主流程 -----------------------------------------------------------

def run_pipeline(
    input_file: str, 
    output_root: str = None,
    device: str = None,
    verbose: bool = True
) -> Tuple[str, List[dict], Dict[str, float]]:
    """
    解析入口。返回 (out_dir, pages_list, time_stats)
    
    Args:
        input_file: 输入文件路径
        output_root: 输出目录（可选）
        device: 设备名称（可选，默认自动检测）
        verbose: 是否显示详细信息
        
    Returns:
        (out_dir, pages_list, time_stats)
    """
    if device is None:
        device = DEFAULT_DEVICE
    
    if verbose:
        print(f"🔧 使用设备: {device}")
    
    # 创建新的 pipeline 实例
    pipeline = create_pipeline("PP-StructureV3", device=device)
    
    return run_pipeline_with_model(
        input_file, 
        output_root, 
        pipeline,
        verbose=verbose
    )


def run_pipeline_with_model(
    input_file: str,
    output_root: str = None,
    pipeline = None,
    device: str = None,
    verbose: bool = True
) -> Tuple[str, List[dict], Dict[str, float]]:
    """
    使用指定的 pipeline 实例解析文档。

    Args:
        input_file: 输入文件路径
        output_root: 输出目录
        pipeline: PP-StructureV3 pipeline 实例，如果为 None 则创建新实例
        device: 设备名称，仅在pipeline为None时使用
        verbose: 是否显示详细信息

    Returns:
        (out_dir, pages_list, time_stats)
    """
    in_path = Path(input_file).expanduser().resolve()
    if not in_path.is_file():
        raise FileNotFoundError(f"文件不存在: {in_path}")

    # 如果没有传入 pipeline，则创建新实例
    if pipeline is None:
        if device is None:
            device = DEFAULT_DEVICE
        if verbose:
            print(f"🔧 创建新pipeline，使用设备: {device}")
        pipeline = create_pipeline("PP-StructureV3", device=device)

    # 记录文档转换时间
    doc_conversion_time = None

    # 如是 doc/docx - 使用WPS在线服务转PDF
    if in_path.suffix.lower() in {".doc", ".docx"}:
        if not HAS_WPS_CONVERTER:
            raise RuntimeError(
                "Word文档需要转换为PDF，但未安装wps_word2pdf模块\n"
                "请先手动转换为PDF，或安装: pip install wps_word2pdf"
            )
        if verbose:
            print(f"📄 转换Word文档: {in_path.name}")
        tmp_dir = Path(tempfile.mkdtemp(prefix="doc2pdf_"))
        in_path, doc_conversion_time = _doc_to_pdf(in_path, tmp_dir)
        if verbose:
            print(f"✅ 转换完成，耗时: {doc_conversion_time:.2f}ms")

    if in_path.suffix.lower() != ".pdf":
        raise RuntimeError("仅支持 PDF 或 DOC/DOCX 文件")

    pdf_name = in_path.stem
    out_root = Path(output_root) if output_root else Path(f"output/{pdf_name}")
    (out_root / "imgs").mkdir(parents=True, exist_ok=True)

    merged_md_parts, catalog_done, pages_out = [], False, []

    if verbose:
        print(f"📖 开始解析PDF: {in_path.name}")
    
    # 解析每一页
    for page_no, res in tqdm(
        enumerate(
            pipeline.predict(
                str(in_path),
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
            )
        ),
        desc="解析页面",
        disable=not verbose
    ):
        pg_idx = res.json["res"].get("page_index", page_no)
        pg_dir = out_root / f"page_{pg_idx:03d}"
        img_dir = pg_dir / "images"
        img_dir.mkdir(parents=True, exist_ok=True)

        md_text = res.markdown["markdown_texts"]
        if pg_idx == 0:
            md_text = "【封面】\n" + md_text
        if (not catalog_done) and ("目录" in md_text):
            md_text = md_text.replace("目录", "【目录页】\n目录", 1)
            catalog_done = True

        # 提取页眉页脚
        header = footer = ""
        for blk in res.json["res"].get("parsing_res_list", []):
            if blk["block_label"] == "header":
                header = blk["block_content"]
            elif blk["block_label"] == "footer":
                footer = blk["block_content"]

        md_text = md_text.rstrip("\n") + f"\n<<<页眉:{header};页脚:{footer};页数:{pg_idx + 1}>>>\n"
        md_text = fix_image_path(md_text, pg_idx)

        # 保存Markdown
        (pg_dir / f"page_{pg_idx:03d}.md").write_text(md_text, encoding="utf-8")
        pages_out.append({"page": pg_idx + 1, "content": md_text})

        # 保存 JSON
        (pg_dir / f"page_{pg_idx:03d}.json").write_text(
            json.dumps(res.json, ensure_ascii=False, indent=2), 
            encoding="utf-8"
        )

        # 保存图片
        for rel_path, pil_img in (res.markdown.get("markdown_images") or {}).items():
            local_path = img_dir / rel_path
            local_path.parent.mkdir(parents=True, exist_ok=True)
            pil_img.save(local_path)
            new_ref = process_image(pg_idx, local_path, out_root / "imgs")
            if new_ref:
                md_text = md_text.replace(
                    str(local_path).replace(str(pg_dir) + "/", ""), 
                    new_ref
                )

        merged_md_parts.append({
            "markdown_texts": md_text,
            "page_continuation_flags": res.markdown["page_continuation_flags"],
        })

    # 获取时间统计
    time_stats = dict(pipeline._time_stats) if hasattr(pipeline, '_time_stats') else {}

    # 如果有文档转换时间，添加到统计中
    if doc_conversion_time is not None:
        time_stats['doc_conversion'] = doc_conversion_time

    # 合并 Markdown
    if verbose:
        print("📝 合并Markdown...")
    
    merged_md = pipeline.concatenate_markdown_pages(merged_md_parts)
    
    try:
        merged_md = re.sub(
            r"<table(.|\n)*?</table>",
            lambda m: "\n" + html_fragment_to_md(m.group(0)) + "\n",
            merged_md,
            flags=re.I,
        )
    except RecursionError:
        if verbose:
            print("⚠️  HTML → Markdown 递归过深，已跳过转换")
    except Exception as e:
        if verbose:
            print(f"⚠️  合并 Markdown 时出错: {type(e).__name__}，保留原始内容")

    (out_root / "merged.md").write_text(merged_md, encoding="utf-8")

    return str(out_root.resolve()), pages_out, time_stats


# ---------------- CLI -----------------
if __name__ == "__main__":
    import argparse

    # 打印命令
    command = ' '.join(['python'] + sys.argv)
    print(command)

    parser = argparse.ArgumentParser(
        description="PDF / DOC / DOCX → Markdown 转换器 (支持MetaX GPU)"
    )
    parser.add_argument("input_file", help="源文件路径（pdf/doc/docx）")
    parser.add_argument(
        "-o", "--out", 
        dest="output_root",
        help="自定义输出目录（可选）"
    )
    parser.add_argument(
        "-d", "--device", 
        dest="device", 
        default=None,
        help=f"指定设备 (默认: 自动检测，当前为 {DEFAULT_DEVICE})"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="静默模式，不显示详细信息"
    )
    
    args = parser.parse_args()

    # 打印设备信息
    if not args.quiet:
        try:
            import paddle
            print(f"\n🔧 PaddlePaddle版本: {paddle.__version__}")
            custom_devices = paddle.device.get_all_custom_device_type()
            if custom_devices:
                print(f"🔧 可用自定义设备: {custom_devices}")
            if paddle.device.is_compiled_with_cuda():
                print(f"🔧 CUDA可用: 是")
            device_to_use = args.device if args.device else DEFAULT_DEVICE
            print(f"🔧 使用设备: {device_to_use}\n")
        except Exception as e:
            print(f"⚠️  设备信息获取失败: {e}\n")

    try:
        # 调用主函数
        start_time = time.time()
        
        out_dir, _, time_stats = run_pipeline(
            args.input_file, 
            args.output_root,
            device=args.device,
            verbose=not args.quiet
        )

        total_time = time.time() - start_time

        # 打印时间统计
        if not args.quiet and time_stats:
            print("\n⏱  时间统计:")
            for key, value in time_stats.items():
                if isinstance(value, (int, float)):
                    print(f"  - {key}: {value:.2f}ms")
                else:
                    print(f"  - {key}: {value}")
            print(f"  - 总耗时: {total_time:.2f}秒")

        print(f"\n✅ 完成！输出目录: {out_dir}")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        if not args.quiet:
            traceback.print_exc()
        sys.exit(1)
