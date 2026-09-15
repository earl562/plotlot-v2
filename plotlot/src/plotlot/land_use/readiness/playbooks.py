"""Starter checklists, not jurisdiction-specific legal or technical standards."""
from typing import Literal

from .models import Requirement

Playbook = Literal["residential", "industrial", "data_center"]


def requirements_for(kind: Playbook) -> list[Requirement]:
    if kind not in ("residential", "industrial", "data_center"):
        raise ValueError("Unsupported playbook")
    labels = [
        ("identity", "site_identity", "Parcel and acquisition boundary established"),
        ("zoning", "zoning", "Proposed use and governing approvals reviewed"),
        ("access", "access", "Legal and physical access established for the proposal"),
        ("flood", "flood", "Site-specific flood constraints reviewed for the proposal"),
        ("wetlands", "wetlands", "Site-specific wetland constraints reviewed"),
        ("environmental", "environmental", "Environmental diligence reviewed by responsible professional"),
        ("geotechnical", "geotechnical", "Site-specific geotechnical findings reviewed"),
        ("utilities", "utilities", "Required utility service and conditions documented"),
    ]
    if kind == "data_center":
        labels.extend([
            ("power", "utilities", "Required power capacity, phases, dates, and conditions documented"),
            ("water", "utilities", "Proposed cooling and water requirements verified"),
            ("generation", "environmental", "Proposed generation and associated permit pathway reviewed"),
        ])
    return [Requirement(id=key, category=category, label=label, expected=True)
            for key, category, label in labels]
