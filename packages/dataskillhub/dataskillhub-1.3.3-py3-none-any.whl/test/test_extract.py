from dataskillhub.extract import (
    ExportConfig,
    DossierCompetence,
    flat_export,
)


# part test


def test_flat_export():
    config = ExportConfig(
        name="Pipo", post="data scientist", trigrammatic=["PPI", "PLP"]
    )
    body_dict = {
        "valeur_ajoutee": "src/valeur_ajoutee.md",
        "competences_cles": "src/competences_cles.md",
        "diplomes": "src/diplomes.md",
        "certifications_formations": "src/certifications_formations.md",
        "langues": "src/langues.md",
        "animateur": "src/animateur.md",
        "missions_significatives": "src/missions_significatives.md",
    }
    dc_list = [
        DossierCompetence(identity="PPI", post="data scientist", body=body_dict), # noqa:
        DossierCompetence(identity="PLP", post="data scientist", body=body_dict), # noqa:
        DossierCompetence(identity="Pipo", post="data scientist", body=body_dict),# noqa:
    ]
    assert flat_export(config, "src") == dc_list
