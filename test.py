# test_all_15_models.py
from paddlex import create_model
import time

# 所有15个模型
models = [
    "PP-LCNet_x1_0_doc_ori",
    "UVDoc",
    "PP-DocBlockLayout",
    "PP-DocLayout_plus-L",
    "PP-LCNet_x1_0_textline_ori",
    "PP-OCRv5_server_det",
    "PP-OCRv5_server_rec",
    "PP-OCRv4_server_seal_det",
    "PP-LCNet_x1_0_table_cls",
    "SLANeXt_wired",
    "SLANet_plus",
    "RT-DETR-L_wired_table_cell_det",
    "RT-DETR-L_wireless_table_cell_det",
    "PP-FormulaNet_plus-L",
    "PP-Chart2Table"
]

print(f"开始测试 {len(models)} 个模型...\n")

success = 0
failed = 0

for i, model_name in enumerate(models, 1):
    print(f"[{i}/{len(models)}] 测试 {model_name}...")
    
    try:
        start = time.time()
        
        model = create_model(
            model_name=model_name,
            device="metax_gpu:0"
        )
        
        output = model.predict("test.jpg")
        for res in output:
            res.print()
        
        elapsed = int((time.time() - start) * 1000)
        print(f"✅ {model_name} 测试成功! 耗时: {elapsed}ms\n")
        success += 1
        
    except Exception as e:
        print(f"❌ {model_name} 测试失败!")
        print(f"错误: {str(e)[:100]}\n")
        failed += 1

print("=" * 60)
print(f"测试完成! 成功: {success}/{len(models)}, 失败: {failed}/{len(models)}")
print("=" * 60)
