from sqlalchemy.orm import joinedload
from typing import Type, List, Optional
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select

class SQLHandler:

    def __init__(self, db_path, reset_db=False) -> None:
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.reset = reset_db

        if self.reset:
            SQLModel.metadata.drop_all(self.engine)
            SQLModel.metadata.create_all(self.engine)

    def check_exists(self, model: Type[SQLModel], filters: dict) -> bool:
        """
        Check if a record exists in the database based on filters.

        Args:
            model (SQLModel): The model class to query.
            filters (dict): A dictionary of field names and values to filter by.

        Returns:
            bool: True if a record exists, False otherwise.
        """
        with Session(self.engine) as session:
            resp = self.retrieve( model, filters)
            return len(resp) > 0

    def insert(self, model_instance: SQLModel, refresh=False) -> Optional[SQLModel]:
        """
        Insert a new record into the database, if it doesn't already exist.
        Returns the inserted instance or None if it already exists.
        """
        model = type(model_instance)
        filters = {
                    "id": model_instance.id, # Composite key item #1
                    "term":model_instance.term # Composite key item #2
                   } 

        # Handle their respective composit keys
        if model == Section:
            filters["section"] = model_instance.section 
            
        if self.check_exists(model, filters):
            return None
        else:
            with Session(self.engine) as session:
                session.add(model_instance)
                session.commit()
                if refresh:
                    session.refresh(model_instance)
                return model_instance


    def needs_update(self, model: Type[SQLModel], filters: dict, updates: dict) -> bool:
        """
        Check if a record in the database needs to be updated based on the provided information.

        Args:
            model (SQLModel): The model class to query.
            filters (dict): A dictionary of field names and values to filter by.
            updates (dict): A dictionary of field names and their desired values.

        Returns:
            bool: True if the record needs to be updated, False otherwise.
        """
        with Session(self.engine) as session:
            # Retrieve the existing record based on filters
            query = select(model)
            for key, value in filters.items():
                query = query.where(getattr(model, key) == value)
            record = session.exec(query).first()

            if not record:
                return False

            # Compare existing values with the updates
            for key, value in updates.items():
                if getattr(record, key) != value:
                    return True  # Update needed

        return False  # No updates needed

    def update(self, model: Type[SQLModel], filters: dict, updates: dict) -> bool:
        """
        Update a record in the database based on filters.
        """
        with Session(self.engine) as session:
            # Retrieve the record based on filters
            query = select(model)
            for key, value in filters.items():
                query = query.where(getattr(model, key) == value)
            record = session.exec(query).first()

            if record:
                # Apply updates
                for key, value in updates.items():
                    setattr(record, key, value)
                session.add(record)
                session.commit()
                return True
            
        return False

    def remove(self, model: Type[SQLModel], filters: dict) -> bool:
        """
        Remove a record from the database based on filters.
        """
        with Session(self.engine) as session:
            query = select(model)
            for key, value in filters.items():
                query = query.where(getattr(model, key) == value)
            record = session.exec(query).first()

            if record:
                session.delete(record)
                session.commit()
                return True

        return False

    def retrieve(
        self, model: Type[SQLModel], filters: dict = None, join_course: bool = False
    ) -> List[SQLModel]:
        """
        Retrieve records from the database based on optional filters.
        Optionally include related Course when retrieving Section.
        
        Args:
            model (Type[SQLModel]): The model to query.
            filters (dict, optional): Filters to apply to the query.
            join_course (bool, optional): Whether to include related Course when retrieving Section.

        Returns:
            List[SQLModel]: List of retrieved records.
        """
        with Session(self.engine) as session:
            query = select(model)
            
            # Include the related Course if the model is Section and join_course is True
            if join_course and model is Section:
                query = query.options(joinedload(Section.course))
            
            if filters:
                for key, value in filters.items():
                    query = query.where(getattr(model, key) == value)
            
            return session.exec(query).all()

    def summary(self) -> dict:
        """
        Retrieve a summary of the database, including the number of courses and sections.
        """
        with Session(self.engine) as session:
            course_count = session.exec(select(Course)).all()
            section_count = session.exec(select(Section)).all()
            return {
                "course_count": len(course_count),
                "section_count": len(section_count),
            }
    
class Course(SQLModel, table=True):
    id: str = Field(max_length=10, primary_key=True)  # Primary key
    term: str = Field(max_length=4, primary_key=True) # This needs to be composite too!
    season: str = Field(max_length=10, default=None)
    year: int = Field(default=None)
    sub: str = Field(max_length=10, default=None)
    nbr: str = Field(max_length=4, default=None)
    ending: Optional[str] = Field(max_length=1, default=None, nullable=True)
    search_code: str = Field(max_length=15, default=None)

    # Relationship to Section
    sections: List["Section"] = Relationship(back_populates="course")

class Section(SQLModel, table=True):
    id: str = Field(foreign_key="course.id", primary_key=True)  # Foreign key to Course
    term: str = Field(max_length=4, primary_key=True) # This needs to be composite too!
    section: str = Field(max_length=3, default=None, primary_key=True) # One more composite for this one sadly
    instructor: Optional[str] = Field(max_length=255, default=None)
    A: Optional[int] = Field(default=None)
    B: Optional[int] = Field(default=None)
    C: Optional[int] = Field(default=None)
    D: Optional[int] = Field(default=None)
    F: Optional[int] = Field(default=None)
    AU: Optional[int] = Field(default=None)
    P: Optional[int] = Field(default=None)
    NG: Optional[int] = Field(default=None)
    W: Optional[int] = Field(default=None)
    I: Optional[int] = Field(default=None)
    IP: Optional[int] = Field(default=None)
    Pending: Optional[int] = Field(default=None)
    Total: Optional[int] = Field(default=None)

    # Relationship to Course
    course: Optional[Course] = Relationship(back_populates="sections")

def _main():
    handler = SQLHandler(db_path="database/othertest.db", reset=True)

if __name__ == "__main__":
    _main()