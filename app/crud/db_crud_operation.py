
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, select
from typing import List, Dict, Any, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session



def create_model_entry_sync(db:Session, data: dict, model: Any):
    """
    Create a new User record.
    :param db: SQLAlchemy session
    :param user_data: Dictionary containing the User data
    :return: The created User instance
    """
    database = model(**data)
    try:
        db.add(database)
        db.commit()
        db.refresh(database)
        return database
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Error creating user: {e.orig}")

async def create_model_entry(db:AsyncSession, data: dict, model: Any ):
    """
    Asynchronously create a new record in the given model.
    """
    database = model(**data)
    try:
        db.add(database)
        await db.commit()
        await db.refresh(database)
        return database
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Error creating user: {e.orig}")


# Generic function to get an entry by ID
def get_model_entry(db:Session, filter_data: dict, model: Any):
    """
    Retrieve a record from the User model based on filter criteria.
    :param db: SQLAlchemy session
    :param filter_data: Dictionary containing the criteria to filter the record(s)
    :return: The last matching record instance or None if not found
    """
    try:
        return db.query(model).filter_by(**filter_data).order_by(model.id.desc()).first()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


# Generic function to fetch all entries with pagination

async def fetch_model_entries(
        db: AsyncSession,
        model: Any,
        join_model: Optional[Type] = None,
        filter_data: Optional[Dict[str, Any]] = None,
        exclude_data: Optional[Dict[str, Any]] = None,
        aggregate_data: Optional[Dict[str, str]] = None,
        order_by: Optional[List[str]] = None,
        latest_by_field: Optional[str] = None,
        group_by: Optional[List[str]] = None,
        skip: int = 0,
        limit: Optional[int] = None,
        fetch_one: bool = False,
        options: Optional[List[Any]] = None
) -> Any:
    """
    Asynchronously retrieve multiple records from the given model with optional joins, filtering, exclusion, aggregation, ordering, grouping, and pagination.
    """
    query = select(model)

    # ✅ Apply eager loading if options are provided
    if options:
        for opt in options:
            query = query.options(opt)

    # Apply join if join_model is provided
    if join_model:
        query = query.join(join_model)

    # Apply filters
    if filter_data:
        filters = []
        for key, value in filter_data.items():
            if key.find('__'):
                field_name = key.split('__')[0]
            else:
                field_name = key

            if '.' in field_name:
                model_name, field = field_name.split('.')
                if model_name == model.__name__:
                    field_attr = getattr(model, field)
                elif join_model and model_name == join_model.__name__:
                    field_attr = getattr(join_model, field)
                else:
                    raise ValueError(f"Unknown model name '{model_name}' in filter key.")
            else:
                field_attr = getattr(model, field_name)

            # Handle different operators

            if key.endswith('__in'):
                filters.append(field_attr.in_(value))
            elif key.endswith('__gte'):
                filters.append(field_attr >= value)
            elif key.endswith('__lte'):
                filters.append(field_attr <= value)
            elif key.endswith('__gt'):
                filters.append(field_attr > value)
            elif key.endswith('__lt'):
                filters.append(field_attr < value)
            elif key.endswith('__ilike'):
                filters.append(field_attr.ilike(value))
            else:
                # Default to equality
                filters.append(field_attr == value)

        query = query.where(*filters)

    # Apply exclusions
    if exclude_data:
        for key, value in exclude_data.items():
            if hasattr(model, key):
                query = query.where(getattr(model, key) != value)
            elif join_model and hasattr(join_model, key):
                query = query.where(getattr(join_model, key) != value)

    # Apply latest_by_field logic
    if latest_by_field:
        subquery = (
            select(
                getattr(model, latest_by_field).label(latest_by_field),
                func.max(getattr(model, "created_at")).label("latest_created_at")
            )
            .group_by(getattr(model, latest_by_field))
            .subquery()
        )
        query = query.join(
            subquery,
            (getattr(model, latest_by_field) == subquery.c[latest_by_field]) &
            (getattr(model, "created_at") == subquery.c.latest_created_at)
        )

    # Apply aggregations
    if aggregate_data:
        select_columns = []
        for field, agg_func in aggregate_data.items():
            field_attr = getattr(model, field)
            if agg_func == 'count':
                select_columns.append(func.count(field_attr).label(f"{field}_count"))
            elif agg_func == 'sum':
                select_columns.append(func.sum(field_attr).label(f"{field}_sum"))
            elif agg_func == 'avg':
                select_columns.append(func.avg(field_attr).label(f"{field}_avg"))
            elif agg_func == 'min':
                select_columns.append(func.min(field_attr).label(f"{field}_min"))
            elif agg_func == 'max':
                select_columns.append(func.max(field_attr).label(f"{field}_max"))
        query = query.with_only_columns(*select_columns)  # ✅ Corrected

    # Apply grouping
    if group_by:
        query = query.group_by(*[getattr(model, field) for field in group_by])

    # Apply ordering
    if order_by:
        order_criteria = []
        for field in order_by:
            if field.startswith('-'):
                order_criteria.append(getattr(model, field[1:]).desc())
            else:
                order_criteria.append(getattr(model, field).asc())
        query = query.order_by(*order_criteria)

    # Apply pagination
    if skip:
        query = query.offset(skip)
    if limit:
        query = query.limit(limit)

    # Execute query
    result = await db.execute(query)

    if fetch_one:
        return result.scalars().first()# Fetch single record

    return result.scalars().all()  # Fetch multiple records


def fetch_model_entries_sync(
    db:Session,
    model: Any,
    join_model: Optional[Type] = None,
    filter_data: Optional[Dict[str, Any]] = None,
    exclude_data: Optional[Dict[str, Any]] = None,
    aggregate_data: Optional[Dict[str, str]] = None,
    order_by: Optional[List[str]] = None,
    group_by: Optional[List[str]] = None,
    skip: int = 0,
    limit: Optional[int] = None,
    fetch_one: bool = False  # New parameter to determine whether to fetch one or multiple records
) -> Any:
    """
    Retrieve multiple records from the given model with optional joins, filtering, exclusion, aggregation, ordering, grouping, and pagination.

    :param db: SQLAlchemy session
    :param model: SQLAlchemy model class
    :param join_model: SQLAlchemy model class to join with (optional)
    :param filter_data: Dictionary of field-value pairs to filter by
    :param exclude_data: Dictionary of field-value pairs to exclude
    :param aggregate_data: Dictionary of field-aggregate function pairs
    :param order_by: List of fields to order by (prefix with '-' for descending order)
    :param group_by: List of fields to group by
    :param skip: Number of records to skip
    :param limit: Maximum number of records to return
    :param fetch_one: Boolean flag to return a single record instead of a list
    :return: A single record instance or a list of record instances or aggregated results
    """

    query = db.query(model)

    # Apply join if join_model is provided
    if join_model:
        query = query.join(join_model)

    # Apply filters
    if filter_data:
        filters = []
        for key, value in filter_data.items():
            # Check if the key uses '__in' logic
            if key.endswith('__in'):
                field_name = key.split('__')[0]
            else:
                field_name = key

            # Handle 'Model.field' notation for filtering across models
            if '.' in field_name:
                model_name, field = field_name.split('.')

                # Check if the field belongs to the main model
                if model_name == model.__name__:
                    field_attr = getattr(model, field)
                # Check if the field belongs to the joined model
                elif join_model and model_name == join_model.__name__:
                    field_attr = getattr(join_model, field)
                else:
                    raise ValueError(f"Unknown model name '{model_name}' in filter key.")
            else:
                # Handle normal field filtering without model prefix
                field_attr = getattr(model, field_name)

            # Apply '__in' filter or standard equality filter
            if key.endswith('__in'):
                filters.append(field_attr.in_(value))
            else:
                filters.append(field_attr == value)

        query = query.filter(*filters)

    # Apply exclusions
    if exclude_data:
        for key, value in exclude_data.items():
            if hasattr(model, key):
                query = query.filter(getattr(model, key) != value)
            elif join_model and hasattr(join_model, key):
                query = query.filter(getattr(join_model, key) != value)

    # Apply aggregations
    if aggregate_data:
        select_columns = []
        for field, agg_func in aggregate_data.items():
            field_attr = getattr(model, field)
            if agg_func == 'count':
                select_columns.append(func.count(field_attr).label(f"{field}_count"))
            elif agg_func == 'sum':
                select_columns.append(func.sum(field_attr).label(f"{field}_sum"))
            elif agg_func == 'avg':
                select_columns.append(func.avg(field_attr).label(f"{field}_avg"))
            elif agg_func == 'min':
                select_columns.append(func.min(field_attr).label(f"{field}_min"))
            elif agg_func == 'max':
                select_columns.append(func.max(field_attr).label(f"{field}_max"))
        query = query.with_entities(*select_columns)

    # Apply grouping
    if group_by:
        query = query.group_by(*[getattr(model, field) for field in group_by])

    # Apply ordering
    if order_by:
        order_criteria = []
        for field in order_by:
            if field.startswith('-'):
                order_criteria.append(getattr(model, field[1:]).desc())
            else:
                order_criteria.append(getattr(model, field).asc())
        query = query.order_by(*order_criteria)

    # Apply pagination
    if skip:
        query = query.offset(skip)
    if limit:
        query = query.limit(limit)

    # Execute the query
    if fetch_one:
        return query.first()  # Return the first record
    else:
        return query.all()  # Return the list of records
    # Return the list of records


# Generic function to update an entry
def update_model_entry(db:Session, update_data: dict, filter_data: dict, model: Any):
    """
    Update a record by ID in the given model.
    :param db: SQLAlchemy session
    :param model: SQLAlchemy model class
    :param entry_id: ID of the record to update
    :param update_data: Dictionary containing the data to update
    :return: The updated record instance
    """
    entry = db.query(model).filter_by(**filter_data).first()
    if not entry:
        raise ValueError(f"Record with ID not found")

    for key, value in update_data.items():
        setattr(entry, key, value)
    try:
        db.commit()
        db.refresh(entry)
        return entry
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Error updating entry: {e.orig}")


def create_model_object(data: dict,  model: Any):
    return model(**data)

