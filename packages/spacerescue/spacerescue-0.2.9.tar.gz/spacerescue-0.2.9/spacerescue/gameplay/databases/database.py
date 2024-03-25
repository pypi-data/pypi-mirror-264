import logging
import os
import random
import zipfile
import duckdb
import numpy as np

from spacerescue.physic.galaxy.galaxy import Galaxy
from spacerescue.physic.galaxy.hyperspace_portal import HyperspacePortal
from spacerescue.physic.galaxy.planet import Planet
from spacerescue.physic.galaxy.star import Star
from spacerescue.resources import GLOBAL_RESOURCES
from spacerescue.tools.util import secret_token


class Database:

    MISSIONS = GLOBAL_RESOURCES.load_res_yaml("missions")
    MESSAGE_MISSION_RESCUE = MISSIONS["message_rescue_mission"]

    reset_database = True

    @staticmethod
    def set_options(reset_database: bool = False):
        Database.reset_database = reset_database

    @staticmethod
    def create_database():
        if os.path.exists("resources/data/spacerescue.db"):
            if not Database.reset_database:
                return
            os.remove("resources/data/spacerescue.db")

        logging.info("INFO: CONTEXT: Unpacking data ...")
        with zipfile.ZipFile("resources/data/spacerescue.db.zip", "r") as zip_ref:
            zip_ref.extractall("resources/data/")

        con = duckdb.connect("resources/data/spacerescue.db")
        con.execute(
            """
                CREATE TABLE IDDB (
                    id INTEGER,
                    token VARCHAR
                )"""
        )
        con.close()

    @staticmethod
    def create_mldb_table(rescue_planet: Planet):
        assert rescue_planet.parent is not None
        if not Database.reset_database:
            return

        logging.info("INFO: CONTEXT: [MLDB] Build database ...")
        con = duckdb.connect("resources/data/spacerescue.db")

        count = con.sql("SELECT COUNT(*) FROM MLDB").fetchone()
        assert count is not None

        message_id = np.random.randint(0, count[0])
        content = (
            Database.MESSAGE_MISSION_RESCUE.replace("{PLANET_NAME}", rescue_planet.name)
            .replace("{STAR_SYSTEM_NAME}", rescue_planet.parent.name)
            .replace("{STAR_DATE}", str(random.getrandbits(32)))
        )
        con.execute(f'UPDATE MLDB SET content=\'{content}\' WHERE id={message_id}')

        con.close()

    @staticmethod
    def create_sodb_table(galaxy: Galaxy):
        if not Database.reset_database:
            return

        con = duckdb.connect("resources/data/spacerescue.db")
        logging.info("INFO: CONTEXT: [SODB] Build database ...")
        for id, so in enumerate(galaxy.stellar_objects):
            x, y, z = so.position
            if isinstance(so, Star):
                name = so.name
                parent_id = id
                type = "star"
            elif isinstance(so, Planet) and so.parent is not None:
                name = so.name
                parent_id = galaxy.stellar_objects.index(so.parent)
                type = "planet"
            elif isinstance(so, HyperspacePortal) and so.parent is not None:
                name = so.name
                parent_id = galaxy.stellar_objects.index(so.parent)
                type = "portal"
            else:
                continue
            con.execute(
                f"INSERT INTO SODB VALUES({id}, {parent_id}, '{name}', '{type}', {x}, {y}, {z})"
            )
        con.close()

    @staticmethod
    def create_htdb_table(galaxy: Galaxy):
        if not Database.reset_database:
            return

        con = duckdb.connect("resources/data/spacerescue.db")
        logging.info("INFO: CONTEXT: [HTDB] Build database ...")
        for row in range(0, galaxy.hyperspace_edges.shape[0]):
            for col in range(0, galaxy.hyperspace_edges.shape[1]):
                if galaxy.hyperspace_edges[row, col]:
                    id1 = galaxy.hyperspace_indices[row]
                    id2 = galaxy.hyperspace_indices[col]
                    risk = np.random.rand()
                    con.execute(f"INSERT INTO HTDB VALUES({id1}, {id2}, {risk})")
        con.close()

    @staticmethod
    def create_iddb_table():
        if not Database.reset_database:
            return

        logging.info("INFO: CONTEXT: [IDDB] Build database ...")
        con = duckdb.connect("resources/data/spacerescue.db")
        for i in range(100):
            token = secret_token(4)
            con.execute(f"INSERT INTO IDDB VALUES({i}, '{token}')")
        con.close()
