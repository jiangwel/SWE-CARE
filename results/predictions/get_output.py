import json
import os
import sys
import re

def main():
    # Input file path
    input_file_path = "/Users/jiangwei/Develop/Github/SWE-CARE/results/predictions/out.txt"
    # Target file path
    output_file_path = "/Users/jiangwei/Develop/Github/SWE-CARE/results/predictions/res.jsonl"
    
    if not os.path.exists(input_file_path):
        print(f"输入文件不存在: {input_file_path}")
        sys.exit(1)

    try:
        with open(input_file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"读取输入文件出错: {e}")
        sys.exit(1)

    # Parse content using regex
    # Format: [instance_id][review_text] separated by newlines
    pattern = r'\[([^\]\n]+)\]\[([\s\S]*?)\](?=\n\s*\[|\Z)'
    matches = re.findall(pattern, content)

    if not matches:
        print("未在输入文件中找到符合格式 [instance_id][review_text] 的内容。")
        return

    print(f"找到 {len(matches)} 条记录。")

    # Ensure output directory exists
    try:
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    except OSError as e:
        print(f"创建输出目录失败: {e}")
        sys.exit(1)

    # Load existing instance_ids to avoid duplicates
    existing_ids = set()
    if os.path.exists(output_file_path):
        try:
            with open(output_file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if "instance_id" in data:
                            existing_ids.add(data["instance_id"])
                    except json.JSONDecodeError:
                        pass # Ignore invalid lines
        except Exception as e:
            print(f"读取现有文件出错: {e}")
            # Proceed even if reading fails? Better to warn and maybe stop or continue with empty set
            # For now, let's continue but warn
            print("警告: 无法读取现有文件以检查重复项。")

    count = 0
    try:
        # Check for prefix newline if file is not empty
        prefix = ""
        if os.path.exists(output_file_path) and os.path.getsize(output_file_path) > 0:
            with open(output_file_path, 'rb') as f_check:
                f_check.seek(-1, os.SEEK_END)
                if f_check.read(1) != b'\n':
                    prefix = "\n"
        
        # We need to know if we wrote anything to handle the first prefix correctly
        first_write = True

        with open(output_file_path, "a", encoding="utf-8") as f_out:
            for instance_id, review_text in matches:
                instance_id = instance_id.strip()
                if instance_id in existing_ids:
                    print(f"跳过已存在的记录: {instance_id}")
                    continue

                data = {
                    "instance_id": instance_id,
                    "review_text": review_text, # json.dumps will handle escaping
                    "review_trajectory": None
                }
                json_line = json.dumps(data, ensure_ascii=False)
                
                # write prefix only for the very first write if needed
                if first_write:
                    f_out.write(prefix + json_line + "\n")
                    first_write = False
                    # After the first write, the file definitely ends with \n (from our write)
                    # so subsequent writes don't need the original prefix logic, just newlines
                    # But actually we are appending line by line.
                    # If we write "prefix + json_line + \n", next time we just write "json_line + \n"
                    # But wait, if first_write becomes False, we should just write json_line + "\n"
                    # BUT prefix is only needed ONCE if the file didn't end with newline.
                    # So for subsequent iterations in this loop, prefix should effectively be empty string.
                    prefix = "" 
                else:
                    f_out.write(json_line + "\n")
                
                count += 1
                # Add to existing_ids to prevent duplicates within the same batch
                existing_ids.add(instance_id)
                
        print(f"成功写入 {count} 行到 {output_file_path}")

    except Exception as e:
        print(f"写入文件出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
