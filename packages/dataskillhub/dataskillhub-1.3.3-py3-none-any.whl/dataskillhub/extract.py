from pydantic import BaseModel
from typing import List
import yaml


class ExportConfig(BaseModel):
    name: str
    post: str
    trigrammatic: List[str]


class DossierCompetence(BaseModel):
    identity: str
    post: str
    body: dict


def get_content(source: str) -> str:
    """Read source file contents"""
    with open(source, "r") as content:
        content_str = content.read()
    return content_str


def read_yaml(file_path: str) -> ExportConfig:
    """Read yaml file contents"""
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)
    return ExportConfig(**config)


def flat_export(config: ExportConfig, consultant_path: str) -> list:
    """export to list[DossierCompetence]"""
    identity_list = config.trigrammatic
    identity_list.append(config.name)
    body_dict = {
        "valeur_ajoutee": f"{consultant_path}/valeur_ajoutee.md",
        "competences_cles": f"{consultant_path}/competences_cles.md",
        "diplomes": f"{consultant_path}/diplomes.md",
        "certifications_formations": f"{consultant_path}/certifications_formations.md",  # noqa
        "langues": f"{consultant_path}/langues.md",
        "animateur": f"{consultant_path}/animateur.md",
        "missions_significatives": f"{consultant_path}/missions_significatives.md",  # noqa
    }
    dc_list = []
    for identity in identity_list:
        dc_list.append(
            DossierCompetence(
                identity=identity, post=config.post, body=body_dict
            )  # noqa
        )
    return dc_list


def get_dcs(consultants_path: str, consultant: str) -> list:
    """read all file md in list[DossierCompetence]"""
    consultant_path = f"{consultants_path}/{consultant}"
    config = read_yaml(f"{consultant_path}/export.yaml")
    dc_list = flat_export(config, consultant_path)
    for dc in dc_list:
        for key in dc.body:
            dc.body[key] = get_content(dc.body[key])
    return dc_list
