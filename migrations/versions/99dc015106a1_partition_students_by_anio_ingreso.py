"""partition students by anio_ingreso

Revision ID: 99dc015106a1
Revises: 
Create Date: 2026-06-14 20:31:10.849628

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '99dc015106a1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # 1. Renombra la tabla actual para preservar los datos
    op.execute("ALTER TABLE students RENAME TO students_old")

    # 2. Crea la nueva tabla students particionada por rango de anio_ingreso
    op.execute("""
        CREATE TABLE students (
            id           SERIAL,
            user_id      INTEGER NOT NULL,
            legajo       VARCHAR(20) NOT NULL,
            carrera      VARCHAR(100) NOT NULL,
            anio_ingreso INTEGER NOT NULL,
            PRIMARY KEY (id, anio_ingreso)
        ) PARTITION BY RANGE (anio_ingreso)
    """)

    # 3. Crea las particiones por año de ingreso (2018 a 2025)
    op.execute("CREATE TABLE students_2018 PARTITION OF students FOR VALUES FROM (2018) TO (2019)")
    op.execute("CREATE TABLE students_2019 PARTITION OF students FOR VALUES FROM (2019) TO (2020)")
    op.execute("CREATE TABLE students_2020 PARTITION OF students FOR VALUES FROM (2020) TO (2021)")
    op.execute("CREATE TABLE students_2021 PARTITION OF students FOR VALUES FROM (2021) TO (2022)")
    op.execute("CREATE TABLE students_2022 PARTITION OF students FOR VALUES FROM (2022) TO (2023)")
    op.execute("CREATE TABLE students_2023 PARTITION OF students FOR VALUES FROM (2023) TO (2024)")
    op.execute("CREATE TABLE students_2024 PARTITION OF students FOR VALUES FROM (2024) TO (2025)")
    op.execute("CREATE TABLE students_2025 PARTITION OF students FOR VALUES FROM (2025) TO (2026)")

    # 4. Copia los datos de la tabla vieja a la nueva
    op.execute("""
        INSERT INTO students (id, user_id, legajo, carrera, anio_ingreso)
        SELECT id, user_id, legajo, carrera, anio_ingreso
        FROM students_old
    """)

    # 5. Elimina la tabla vieja
    op.execute("DROP TABLE students_old")


def downgrade() -> None:

    # Revierte el particionado — vuelve a la tabla simple
    op.execute("ALTER TABLE students RENAME TO students_partitioned")

    op.execute("""
        CREATE TABLE students (
            id           SERIAL PRIMARY KEY,
            user_id      INTEGER NOT NULL UNIQUE,
            legajo       VARCHAR(20) NOT NULL UNIQUE,
            carrera      VARCHAR(100) NOT NULL,
            anio_ingreso INTEGER NOT NULL
        )
    """)

    op.execute("""
        INSERT INTO students (id, user_id, legajo, carrera, anio_ingreso)
        SELECT id, user_id, legajo, carrera, anio_ingreso
        FROM students_partitioned
    """)

    op.execute("DROP TABLE students_partitioned CASCADE")