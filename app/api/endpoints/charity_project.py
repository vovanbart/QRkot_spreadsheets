from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_correct_full_amount_for_update,
                                check_name_duplicate, check_project_was_closed,
                                check_project_was_invested)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import execute_investment_process

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Get all the charity projects.
        Endpoint is available for all users.
    """
    charity_projects = await charityproject_crud.get_multiple(session)
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create new Charity Project.
        Endpoint is available only for superusers.
    """
    await check_name_duplicate(
        charity_project.name, session
    )
    new_charity_project = await charityproject_crud.create(
        charity_project, session
    )
    await execute_investment_process(
        new_charity_project, session
    )
    await session.refresh(new_charity_project)
    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
    project_id: int,
    object_is_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Partial update of Charity Project.
        Endpoint is available only for superuser.
        Fields to update:
            - name (should be unique);
            - description;
            - full_amount (could not be less than the invested amount).
    """
    is_charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_project_was_closed(project_id, session)

    if object_is_in.full_amount is not None:
        await check_correct_full_amount_for_update(
            project_id, session, object_is_in.full_amount
        )

    if object_is_in.name is not None:
        await check_name_duplicate(
            object_is_in.name, session
        )

    is_charity_project = await charityproject_crud.update(
        is_charity_project, object_is_in, session
    )
    return is_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Deletion of Charity Project.
        The invested project could only be closed but not deleted.
        Not invested projects could be deleted.
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_project_was_invested(project_id, session)
    charity_project = await (
        charityproject_crud.remove(
            charity_project, session
        )
    )
    return charity_project
