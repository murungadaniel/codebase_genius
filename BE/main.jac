import from byllm.llm { Model }
import from dotenv { load_dotenv }
include supervisor;
include walker_codebase_genius;

with entry {
    load_dotenv();
}