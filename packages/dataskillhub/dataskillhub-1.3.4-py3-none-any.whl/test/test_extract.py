from dataskillhub.extract import (
    Version,
    ExportConfig,
    DossierCompetence,
    flat_export,
)


# part test


def test_flat_export():
    config = ExportConfig(
        post="data scientise",
        versions=[
            Version(name="Pipo", file_id="s", anonymised=False),
            Version(name="PPI", file_id="t1", anonymised=True),
            Version(name="PLP", file_id="t2", anonymised=True),
        ],
    )
    body_dict = {
        "valeur_ajoutee": "ok/valeur_ajoutee.md",
        "competences_cles": "ok/competences_cles.md",
        "diplomes": "ok/diplomes.md",
        "certifications_formations": "ok/certifications_formations.md",
        "langues": "ok/langues.md",
        "animateur": "ok/animateur.md",
        "missions_significatives": "ok/missions_significatives.md",
    }
    dc_list = [
        DossierCompetence(
            identity="Pipo",
            anonyme=False,
            post="data scientise",
            body=body_dict,
            file_id="s",  # noqa
        ),
        DossierCompetence(
            identity="PPI",
            anonyme=True,
            post="data scientise",
            body=body_dict,
            file_id="t1",
        ),
        DossierCompetence(
            identity="PLP",
            anonyme=True,
            post="data scientise",
            body=body_dict,
            file_id="t2",
        ),
    ]
    assert flat_export(config, "ok") == dc_list
