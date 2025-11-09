import from byllm.llm { Model }
import subprocess;
import os;
import json;

glob llm = Model(model_name="gemini/gemini-2.0-flash", verbose=False);

node Supervisor {
    has url: str = "";

    # ============= REGULAR METHODS (INSIDE NODE) =============
    def clone_repo(url: str) -> str {
        if not url.startswith("https://github.com/") or not url.endswith(".git") {
            return "Error: Must be a public GitHub URL ending in .git";
        }
        repo_name = url.split("/")[-1].replace(".git", "");
        path = f"/tmp/codebase_genius_{repo_name}";
        try {
            if os.path.isdir(path) {
                subprocess.run(["rm", "-rf", path], check=True);
            }
            subprocess.run(
                ["git", "clone", "--depth", "1", url, path],
                capture_output=True, text=True, check=True
            );
            return path;
        } except Exception as e {
            return f"Clone failed: {str(e)}";
        }
    }

    def get_file_tree(path: str) -> str {
        if not os.path.isdir(path) {
            return "Error: Invalid path";
        }
        lines = [];
        for walk_result in os.walk(path) {
            root = walk_result[0];
            dirs = walk_result[1];
            files = walk_result[2];
            
            rel_dir = root.replace(path, "").lstrip("/");
            if rel_dir {
                lines.append(f"{rel_dir}/");
            }
            for file in files {
                rel_path = os.path.join(rel_dir, file);
                if any(rel_path.endswith(ext) for ext in [
                    ".py", ".jac", ".js", ".ts", ".java", ".cpp", ".c", ".h",
                    ".md", ".txt", ".json", ".yaml", ".yml"
                ]) {
                    lines.append(f"  {rel_path}");
                }
            }
        }
        return "\n".join(lines) if lines else "No supported files.";
    }

    def read_file_content(path: str) -> str {
        try {
            with open(path, "r", encoding="utf-8") as f {
                content = f.read();
                if len(content) > 12000 {
                    content = content[:12000] + "\n\n... [truncated]";
                }
                return content;
            }
        } except Exception as e {
            return f"Read error: {str(e)}";
        }
    }

    # ============= LLM-POWERED METHODS =============
    def create_map(path: str) -> str by llm(
        method="ReAct",
        tools=[self.get_file_tree]
    );

    def analyze_file(path: str) -> str by llm(
        method="ReAct",
        tools=[self.read_file_content]
    );

    def generate_diagram(map_desc: str, summaries_json: str) -> str by llm(
        method="zero_shot"
    );

    def assemble_docs(sections_json: str) -> str by llm(
        method="zero_shot"
    );

    def orchestrate(url: str) -> str by llm(
        method="ReAct",
        tools=[
            self.clone_repo,
            self.create_map,
            self.analyze_file,
            self.generate_diagram,
            self.assemble_docs
        ]
    );
}
    # ============= SEMANTIC DEFINITIONS =============
    sem create_map = """
    1. Call get_file_tree(path) → obtain directory tree.
    2. Identify entry points, core modules, config files.
    3. Return Markdown with a *Priority Files* list (max 8 files, reason).
    """;

    sem analyze_file = """
    1. Call read_file_content(path).
    2. Detect language from extension.
    3. Summarise classes, functions, imports, key logic.
    4. Return a clean Markdown section titled with the file name.
    """;

    sem generate_diagram = """
    Input:
      • map_desc      – high‑level map string
      • summaries_json – JSON array of file‑doc strings
    Output *only* Mermaid code inside a fenced block:
    
    graph TD
       ...
    
    """;

    sem assemble_docs = """
    Input: JSON array of {title, content}
    Build full Markdown:
    • # Codebase Documentation: <repo>
    • ## Overview
    • ## Repository Structure
    • ## File Documentation
    • ## Architecture Diagram
    """;

    sem orchestrate = """
    ReAct loop:
    
    clone_repo(url) → path
    create_map(path) → map_desc (extract priority_files from "### Priority Files")
    For each file_path in priority_files (max 8):
      analyze_file(file_path) → collect section
    generate_diagram(map_desc, json.dumps(sections)) → diagram
    assemble_docs(json.dumps(all_sections))
    Final Answer = full Markdown
    """;

    # ============= ENTRY POINT =============
    can execute with codebase_genius entry {
        response = self.orchestrate(visitor.url);
        report {
            "documentation": response,
            "url": visitor.url
        };
    }




