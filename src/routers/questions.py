from fastapi import HTTPException, APIRouter, Depends
from src import managers
from src.models import QuestionCreate, Question, QuestionWithAnswers
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session

router = APIRouter()


@router.get("/", response_model=list[Question])
async def get_questions(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)
):
    questions = await managers.get_questions(db, offset, limit)
    return questions


@router.get("/{question_id}", response_model=Question)
async def get_question(question_id: int, db: AsyncSession = Depends(get_session)):
    question = await managers.get_question(db, question_id=question_id)
    if question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question {question_id} does not exist.",
        )
    return question


@router.post("/", response_model=QuestionWithAnswers, status_code=201)
async def post_question(
    question: QuestionCreate, db: AsyncSession = Depends(get_session)
):
    return await managers.create_question(db=db, question=question)


@router.delete("/{question_id}")
async def delete_question(question_id: int, db: AsyncSession = Depends(get_session)):
    question = await managers.get_question(db, question_id=question_id)
    if question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question {question_id} does not exist.",
        )
    await db.delete(question)
    await db.commit()
    return {"message": f"Successfully deleted Question {question_id}."}


# @router.put("/questions/{question_id}")
# async def update_question(question_id: int, response_model=schemas.Question, status_code=200)
#    return {"status": "Successfully updated question."}
