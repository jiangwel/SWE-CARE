from datasets import load_dataset
import os
import json
import ast

def main():
    # Load dataset
    print("Loading dataset...")
    train_data = load_dataset("inclusionAI/SWE-CARE", split="test")
    
    output_dir = "/Users/jiangwei/Develop/SWE-CARE/inputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Template
    template_path = "/Users/jiangwei/Develop/SWE-CARE/template_inp.txt"
    with open(template_path, "r") as f:
        template = f.read()

    print(f"Processing {len(train_data)} items...")
    
    for i, item in enumerate(train_data):
        try:
            instance_id = item['instance_id']
            base_commit = item['base_commit']
            problem_statement = item['problem_statement']
            commit_to_review = item['commit_to_review']
            
            # Handle commit_to_review parsing
            commit_to_review_data = {}
            if isinstance(commit_to_review, dict):
                commit_to_review_data = commit_to_review
            elif isinstance(commit_to_review, str):
                try:
                    commit_to_review_data = json.loads(commit_to_review)
                except json.JSONDecodeError:
                    try:
                        commit_to_review_data = ast.literal_eval(commit_to_review)
                    except Exception as e:
                        print(f"Failed to parse commit_to_review for {instance_id}: {e}")
                        continue
            else:
                print(f"Unexpected type for commit_to_review in {instance_id}: {type(commit_to_review)}")
                continue

            patch_to_review = commit_to_review_data.get('patch_to_review', '')
            
            # Fill template
            content = template.replace("{{instance_id}}", str(instance_id))
            content = content.replace("{{base_commit}}", str(base_commit))
            content = content.replace("{{ problem_statement }}", str(problem_statement))
            content = content.replace("{{ commit_to_review.patch_to_review }}", str(patch_to_review))
            
            # Save to file
            file_path = os.path.join(output_dir, str(instance_id))
            with open(file_path, 'w') as f:
                f.write(content)
                
        except Exception as e:
            print(f"Error processing item {i}: {e}")

    print("Done.")

if __name__ == "__main__":
    main()
