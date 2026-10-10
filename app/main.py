from index_manager import ensure_index_exists
from rag_pipeline import answer_question

ensure_index_exists()

question = "In which year did Sagar complete his Intermediate?"
print(answer_question(question))
