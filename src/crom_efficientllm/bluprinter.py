import os
import argparse
from pathlib import Path
from typing import List, Set

# 기본적으로 제외할 디렉토리 및 파일 패턴
DEFAULT_EXCLUDES = {
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".vscode",
    ".idea",
    "node_modules",
    ".env",
    "*.pyc",
    "*.pyo",
    "*.egg-info",
    "dist",
    "build",
}

def generate_tree(directory: Path, excludes: Set[str]) -> (str, List[Path]):
    """디렉토리 구조 트리와 파일 목록을 생성합니다."""
    tree_str = f"```\n{directory.name}/\n"
    file_paths = []
    
    def build_tree(current_path: Path, prefix: str = ""):
        nonlocal tree_str
        # listdir를 사용하여 현재 경로의 내용을 가져옵니다.
        try:
            entries = sorted(os.listdir(current_path))
        except FileNotFoundError:
            return

        # 필터링: 제외 목록에 포함된 항목을 걸러냅니다.
        filtered_entries = []
        for entry in entries:
            if entry not in excludes:
                # 여기서 추가적인 glob 패턴 매칭을 할 수도 있습니다.
                filtered_entries.append(entry)

        for i, entry in enumerate(filtered_entries):
            is_last = i == (len(filtered_entries) - 1)
            connector = "└── " if is_last else "├── "
            tree_str += f"{prefix}{connector}{entry}\n"
            
            new_path = current_path / entry
            if new_path.is_dir():
                new_prefix = prefix + ("    " if is_last else "│   ")
                build_tree(new_path, new_prefix)
            else:
                file_paths.append(new_path)

    build_tree(directory)
    tree_str += "```\n"
    return tree_str, file_paths

def get_file_content(file_path: Path) -> str:
    """파일 내용을 읽어옵니다. 텍스트 파일이 아닐 경우를 대비해 예외 처리를 포함합니다."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "[Error: Could not read file content, possibly a binary file.]\n"

def main():
    parser = argparse.ArgumentParser(description="Generate a project blueprint in a single Markdown file.")
    parser.add_argument("--input-dir", type=str, required=True, help="The root directory of the project to scan.")
    parser.add_argument("--output-file", type=str, default="project_blueprint.md", help="The name of the output Markdown file.")
    args = parser.parse_args()

    input_path = Path(args.input_dir).resolve()
    output_path = Path(args.output_file).resolve()

    print(f"Scanning project at: {input_path}")

    # 1. 디렉토리 구조 및 파일 목록 생성
    tree_structure, file_paths = generate_tree(input_path, DEFAULT_EXCLUDES)

    # 2. 최종 리포트 생성
    with output_path.open("w", encoding="utf-8") as f:
        f.write(f"# Project Blueprint: {input_path.name}\n\n")
        f.write("## 1. Project Directory Tree\n\n")
        f.write(tree_structure)
        f.write("\n## 2. File Contents\n\n")

        for path in file_paths:
            print(f"  - Processing: {path.relative_to(input_path)}")
            f.write(f"---\n### **File:** `{path}`\n")
            
            # 파일 확장자에 따라 코드 블록 언어 지정
            lang = path.suffix.lstrip('.')
            if not lang:
                lang = "text"

            f.write(f"```{lang}\n")
            f.write(get_file_content(path))
            f.write(f"\n```\n\n")

    print(f"\nSuccessfully generated project blueprint at: {output_path}")

if __name__ == "__main__":
    main()
