from typing import Optional

from pydantic import BaseModel


class GuidelineDocument(BaseModel):
    guideline_id: int
    name: str
    description: str
    institution_short_name: str
    publish_date: str

    def __str__(self) -> str:
        fields = [self.name, self.description]
        return "".join([format_field(field) for field in fields])

    def get_oneliner(self) -> str:
        return (
            f"Title: {self.name} (by {self.institution_short_name.upper()}, published "
            f"{self.publish_date.split('T')[0]})"
        )


class InfoBoxDocument(BaseModel):
    rec_id: int
    text: str

    def __str__(self) -> str:
        return format_field(self.text)


class SectionDocument(BaseModel):
    section_id: int
    guideline_doc: GuidelineDocument
    info_box_doc: Optional[InfoBoxDocument] = None
    heading: str
    text: str
    section_label: str
    pico_count: int
    recommendation_count: int
    order: int

    def __str__(self) -> str:
        fields = [self.heading, self.text, self.info_box_doc]
        return "".join([format_field(field) for field in fields])

    def get_oneliner(self) -> str:
        hierarchy_level = len(self.section_label.split("."))
        tabs = "\t" * (hierarchy_level - 1)
        return (
            f"{tabs}Section: "
            f"{(self.section_label + ': ' if hierarchy_level > 1 else '')}"
            f"{self.heading.strip()} ({self.pico_count} PICOs, "
            f"{self.recommendation_count} Recs) "
        )


class RecommendationDocument(BaseModel):
    rec_id: int
    section_doc: SectionDocument
    heading: str
    text: str
    remarks: str
    benefits: str
    evidence: str
    preferences: str
    resources: str
    rational: str
    advice: str
    strength: str
    order: int

    def __str__(self) -> str:
        fields = [
            self.heading,
            self.text,
            self.remarks,
            self.benefits,
            self.evidence,
            self.preferences,
            self.resources,
            self.rational,
            self.advice,
        ]
        return "".join([format_field(field) for field in fields])

    def get_oneliner(self) -> str:
        return (
            f"\t\tRec ({self.strength}): "
            f"{self.text.split('.')[0].split(' (')[0].strip()}"
        )


class PicoDocument(BaseModel):
    pico_id: int
    rec_doc: RecommendationDocument
    population: str
    intervention: str
    comparator: str
    summary: str
    order: int

    def __str__(self) -> str:
        fields = [self.population, self.intervention, self.comparator, self.summary]
        return "".join([format_field(field) for field in fields])

    def get_oneliner(self) -> str:
        return (
            f"\t\t\tPICO: {self.population}, {self.intervention} vs. {self.comparator}"
        )


class DichotomousOutcomeDocument(BaseModel):
    di_outcome_id: int
    pico_doc: PicoDocument
    outcome: str
    summary: str
    quality_indirectness_comment: str
    quality_of_evidence_comment: str
    quality_imprecision_comment: str
    sort_order: int

    def __str__(self) -> str:
        fields = [
            self.pico_doc.rec_doc.section_doc.heading,
            self.outcome,
            self.summary,
            self.quality_indirectness_comment,
            self.quality_of_evidence_comment,
            self.quality_imprecision_comment,
        ]
        return "".join([format_field(field) for field in fields])

    def get_oneliner(self) -> str:
        return f"\t\t\t\tDichotomous outcome: {self.outcome}"


class ContinuousOutcomeDocument(BaseModel):
    co_outcome_id: int
    pico_doc: PicoDocument
    outcome: str
    summary: str
    quality_of_evidence_comment: str
    sort_order: int

    def __str__(self) -> str:
        fields = [
            self.pico_doc.rec_doc.section_doc.heading,
            self.outcome,
            self.summary,
            self.quality_of_evidence_comment,
        ]
        return "".join([format_field(field) for field in fields])

    def get_oneliner(self) -> str:
        return f"\t\t\t\tContinuous outcome: {self.outcome}"


class NonPoolableOutcomeDocument(BaseModel):
    np_outcome_id: int
    pico_doc: PicoDocument
    outcome: str
    summary: str
    quality_of_evidence_comment: str
    sort_order: int

    def __str__(self) -> str:
        fields = [
            self.pico_doc.rec_doc.section_doc.heading,
            self.outcome,
            self.summary,
            self.quality_of_evidence_comment,
        ]
        return "".join([format_field(field) for field in fields])

    def get_oneliner(self) -> str:
        return f"\t\t\t\tNon-poolable outcome: {self.outcome}"


def format_field(field: str):
    if (field is not None) and (str(field) != ""):
        return str(field) + "\n"
    else:
        return ""
