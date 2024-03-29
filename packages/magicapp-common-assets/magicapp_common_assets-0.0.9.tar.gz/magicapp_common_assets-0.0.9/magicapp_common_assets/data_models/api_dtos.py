from enum import Enum
from typing import List, Optional, Tuple

from humps import camelize
from pydantic import BaseModel, HttpUrl


def to_camel(string):
    return camelize(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


##### GUIDELINE ########################################################################
class Guideline(CamelModel):
    # IDs
    guideline_id: int
    current_draft_id: int
    published_id: int

    # Fields we use
    name: str  # Guideline title
    description: str

    # Fields to consider
    language: str
    institution_name: str
    status: str
    default_key_info_type: str

    # Fields we don't use
    by_name: Optional[str] = None
    short_code: str
    owner: str
    main_editor: str
    start_date: str
    last_edit: str
    country_flag: str
    sponsors: str
    disclaimer: str
    isbn: Optional[str] = None
    issn: Optional[str] = None
    org_doc_id: Optional[str] = None
    contact_name: str
    contact_address: str
    contact_email: str
    contact_telephone: str
    contact_web: str
    institution_id: int
    institution_logo_url: str
    institution_short_name: str
    institution_alt_grade: bool
    institution_ga_id: str
    institution_ga4_id: str
    edit: bool
    permission: int
    is_latest_published: bool
    is_draft_editable: bool
    is_public: bool
    version_major: int
    version_minor: int
    draft_pico_count: int
    draft_recommendation_count: int
    published_pico_count: int
    published_recommendation_count: int
    pdf_published_path: str
    pdf_path: Optional[str] = None
    pdf_created_date: Optional[str] = None
    json_path: str
    content_admin: bool
    comments_in_published: bool
    publish_creation_time: str
    publish_date: str
    publish_last_search_date: str
    track_changes: bool
    section_numbers: bool
    show_rec_byline: bool
    show_conflicts: bool
    show_certainty_strength_labels: bool
    show_section_preview: bool
    subscriptions: bool


##### SECTION ##########################################################################
class SectionCounts(CamelModel):
    pico_count: int
    recommendation_count: int


class Section(CamelModel):
    # IDs
    guideline_id: int
    section_id: int
    parent_id: int

    # Fields we use
    heading: str  # Section title
    text: str  # Section content
    counts: SectionCounts

    # Fields to consider
    order: int

    # Fields we don't use
    short_code: str
    section_label: str
    has_children: bool
    has_uncommitted_changes: bool
    links: List[dict] = [{}]


##### RECOMMENDATION ###################################################################
class RecommendationHasData(CamelModel):
    # Fields we use
    recommendation_id: int = None

    # Fields to consider
    advice: bool
    evidence_count: int
    evidence: bool
    interventions: bool
    key_info: bool
    rational: bool
    references: bool

    # Fields we don't use
    more_info: bool
    implementation: bool
    evaluation: bool
    research: bool
    decision_aids: bool
    discussion: bool
    discussion_count: int
    discussion_unresolved_count: int
    key_info_u_c: bool
    emr_codes: bool
    cql_codes: bool
    interventions_u_c: bool
    links: dict = None


class KeyInfoIntervention(CamelModel):
    # IDs
    recommendation_id: int
    pico_id: int

    # Fields we use

    # Fields to consider
    pico_element: str
    intervention: str

    # Fields we don't use
    is_comparator: bool
    show_comparator: bool
    sort_order: int
    judgements: dict
    comparator: bool


class RecommendationKeyInfo(CamelModel):
    # IDs
    guideline_id: Optional[int]
    recommendation_id: int

    # Fields we use
    benefits: str
    evidence: str
    preferences: str
    resources: str

    # Fields to consider
    interventions: List[KeyInfoIntervention]
    key_info_type: str
    benefits_strength: str
    evidence_strength: str
    preferences_strength: str
    resources_strength: str

    # Fields we don't use
    benefits_research_evidence: str
    benefits_research_evidence_in_public: bool
    benefits_additional_consideration: str
    benefits_additional_consideration_in_public: bool
    evidence_research_evidence: str
    evidence_research_evidence_in_public: bool
    evidence_additional_consideration: str
    evidence_additional_consideration_in_public: bool
    preferences_research_evidence: str
    preferences_research_evidence_in_public: bool
    preferences_additional_consideration: str
    preferences_additional_consideration_in_public: bool
    resources_research_evidence: str
    resources_research_evidence_in_public: bool
    resources_additional_consideration: str
    resources_additional_consideration_in_public: bool
    is_summary_of_judgement_public: bool


class RecommendationStrength(Enum):
    INFO = "INFO"
    STRONG = "STRONG"
    WEAK = "WEAK"
    WEAK_AGAINST = "WEAK_AGAINST"
    STRONG_AGAINST = "STRONG_AGAINST"
    ONLY_IN_RESEARCH = "ONLY_IN_RESEARCH"
    NOTSET = "NOTSET"
    PRACTICE = "PRACTICE"
    NO_STRENGTH = "NO_STRENGTH"


class Recommendation(CamelModel):
    # IDs
    guideline_id: int
    section_id: int
    recommendation_id: int

    # Fields we use
    heading: str
    text: str
    rational: str  # Rationale
    has_data: Optional[RecommendationHasData] = None
    key_info: Optional[RecommendationKeyInfo] = None

    # Fields to consider
    order: int
    strength: Optional[RecommendationStrength] = None
    key_info_type: str
    remarks: str
    advice: str
    adaptation: str
    implementation: str
    evaluation: str
    research: str

    # Fields we don't use
    short_code: str
    status: str
    status_date: Optional[str]
    status_comment: Optional[str]
    key_info_display_mode: str
    show_adaptation: bool
    hide_in_publish: bool
    tags: Optional[List[str]]
    links: Optional[List[str]] = [""]


##### PICO #############################################################################
class PicoOutcomeType(Enum):
    DICHOTOMOUS = "DICHOTOMOUS"
    CONTINUOUS = "CONTINUOUS"
    NON_POOLABLE = "NON_POOLABLE"


class PicoOutcomeStatus(Enum):
    DEVELOPMENT = "DEVELOPMENT"
    REVIEW = "REVIEW"
    FINISHED = "FINISHED"
    UPDATE = "UPDATE"


class PicoOutcome(CamelModel):
    # IDs
    pico_id: int
    outcome_id: int

    # Fields we use
    outcome: str
    outcome_type: PicoOutcomeType

    # Fields to consider
    status: PicoOutcomeStatus
    sort_order: int

    # Fields we don't use
    shadow_parent_id: Optional[int]
    short_code: Optional[str] = None
    outcome_short_name: str
    links: List[HttpUrl]


class PicoCodes(CamelModel):
    # IDs
    section_id: int
    pico_id: int
    code_id: int

    # Fields we use

    # Fields to consider
    name: str
    code: str
    description: Optional[str] = None
    ontology: str
    type: str

    # Fields we don't use


class Pico(CamelModel):
    # IDs
    guideline_id: int  # NB! Not part of Magic API schema - added by Sanders
    section_id: int
    recommendation_id: int  # NB! Not part of Magic API schema - added by Sanders
    pico_id: int

    # Fields we use
    population: str
    intervention: str
    comparator: str
    outcomes: List[PicoOutcome]

    # Fields to consider
    order: int
    summary: str
    codes: List[PicoCodes] = None
    has_data: dict
    population_short_name: str
    intervention_short_name: str
    comparator_short_name: str

    # Fields we don't use
    short_code: Optional[str] = None
    usage_count: Optional[int] = None
    links: List[HttpUrl]


class ExtendedPico(Pico):
    recommendation_id: int


##### OUTCOME ##########################################################################
class DichotomousOutcome(CamelModel):
    # IDs
    guideline_id: int  # NB! Not part of Magic API schema - added by Sanders
    section_id: int
    recommendation_id: int  # NB! Not part of Magic API schema - added by Sanders
    pico_id: int
    outcome_id: int

    # Fields we use
    short_name: Optional[str] = None
    quality_indirectness_comment: Optional[str] = None
    quality_of_evidence_comment: Optional[str] = None
    quality_imprecision_comment: Optional[str] = None
    plain_summary_comment: Optional[str] = None

    # Fields to consider
    # Generally all of them! A lot more to be understood. Need an expert for this.

    # Fields we don't use
    status: Optional[str] = None
    is_hidden: Optional[bool] = None
    sort_order: Optional[int] = None
    short_code: Optional[str] = None
    outcome: Optional[str] = None
    time_frame: Optional[str] = None
    importance_level: Optional[str] = None
    intervention_studies: Optional[str] = None
    intervention_total_participants: Optional[float] = None
    intervention_reference_type: Optional[str] = None
    intervention_study_type: Optional[str] = None
    comparator_study_type: Optional[str] = None
    comparator_reference_type: Optional[str] = None
    quality_intervention_study_type: Optional[str] = None
    quality_of_evidence_level: Optional[str] = None
    quality_risk_of_bias: Optional[str] = None
    quality_inconsistency: Optional[str] = None
    quality_indirectness: Optional[str] = None
    quality_imprecision: Optional[str] = None
    quality_publication_bias: Optional[str] = None
    quality_upgrade: Optional[str] = None
    direction_of_effect_type: Optional[str] = None
    absolute_difference: Optional[float] = None
    absolute_difference_direction: Optional[str] = None
    absolute_difference_confidence_type: Optional[str] = None
    absolute_difference_low: Optional[float] = None
    absolute_difference_low_direction: Optional[str] = None
    absolute_difference_high: Optional[float] = None
    absolute_difference_high_direction: Optional[str] = None
    relative_effect: Optional[float] = None
    relative_effect_type: Optional[str] = None
    relative_effect_confidence_type: Optional[str] = None
    relative_effect_confidence_low: Optional[float] = None
    relative_effect_confidence_high: Optional[float] = None
    comparator_effect: Optional[float] = None
    comparator_effect_type: Optional[str] = None
    intervention_effect: Optional[float] = None
    intervention_effect_type: Optional[str] = None
    auto_calc_interventions: Optional[str] = None


class ContinuousOutcome(CamelModel):
    # IDs
    guideline_id: int  # NB! Not part of Magic API schema - added by Sanders
    section_id: int
    recommendation_id: int  # NB! Not part of Magic API schema - added by Sanders
    pico_id: int
    outcome_id: int

    # Fields we use
    short_name: Optional[str] = None
    quality_of_evidence_comment: Optional[str] = None
    plain_summary_comment: Optional[str] = None

    # Fields to consider
    # Generally all of them! A lot more to be understood. Need an expert for this.

    # Fields we don't use
    status: Optional[str] = None
    is_hidden: Optional[bool] = None
    sort_order: Optional[int] = None
    short_code: Optional[str] = None
    outcome: Optional[str] = None
    intervention_reference_type: Optional[str] = None
    intervention_study_type: Optional[str] = None
    comparator_study_type: Optional[str] = None
    comparator_reference_type: Optional[str] = None
    quality_intervention_study_type: Optional[str] = None
    quality_of_evidence_level: Optional[str] = None
    quality_risk_of_bias: Optional[str] = None
    quality_inconsistency: Optional[str] = None
    quality_indirectness: Optional[str] = None
    quality_imprecision: Optional[str] = None
    quality_publication_bias: Optional[str] = None
    quality_upgrade: Optional[str] = None
    direction_of_effect_type: Optional[str] = None
    scale_direction: Optional[str] = None
    intervention_effect_type: Optional[str] = None
    intervention_effect_confidence_type: Optional[str] = None
    comparator_effect_type: Optional[str] = None
    comparator_effect_confidence_type: Optional[str] = None
    absolute_difference_type: Optional[str] = None
    absolute_difference_direction: Optional[str] = None
    absolute_difference_confidence_type: Optional[str] = None
    absolute_difference_low_direction: Optional[str] = None
    absolute_difference_high_direction: Optional[str] = None
    absolute_difference_direction_type: Optional[str] = None


class NonPoolableOutcome(CamelModel):
    # IDs
    guideline_id: int  # NB! Not part of Magic API schema - added by Sanders
    section_id: int
    recommendation_id: int  # NB! Not part of Magic API schema - added by Sanders
    pico_id: int
    outcome_id: int

    # Fields we use
    quality_of_evidence_comment: Optional[str] = None
    plain_summary_comment: Optional[str] = None

    # Fields to consider
    # Generally all of them! A lot more to be understood. Need an expert for this.

    # Fields we don't use
    status: Optional[str] = None
    is_hidden: Optional[bool] = None
    sort_order: Optional[int] = None
    short_code: Optional[str] = None
    outcome: Optional[str] = None
    short_name: Optional[str] = None
    intervention_studies: Optional[str] = None
    intervention_total_participants: Optional[float] = None
    intervention_reference_type: Optional[str] = None
    intervention_study_type: Optional[str] = None
    comparator_study_type: Optional[str] = None
    comparator_reference_type: Optional[str] = None
    quality_intervention_study_type: Optional[str] = None
    quality_of_evidence_level: Optional[str] = None
    quality_risk_of_bias: Optional[str] = None
    quality_inconsistency: Optional[str] = None
    quality_indirectness: Optional[str] = None
    quality_imprecision: Optional[str] = None
    quality_publication_bias: Optional[str] = None
    quality_upgrade: Optional[str] = None
    direction_of_effect_type: Optional[str] = None
    estimates_description: Optional[str] = None


##### COLLECTION #######################################################################
class AllGuidelineDTOs(BaseModel):
    guideline_dto: Guideline
    section_dtos: List[Section]
    recommendation_dtos: List[Recommendation]
    pico_dtos: List[Pico]
    dichotomous_outcome_dtos: List[DichotomousOutcome]
    continuous_outcome_dtos: List[ContinuousOutcome]
    non_poolable_outcome_dtos: List[NonPoolableOutcome]


class OutcomeIDs(BaseModel):
    di_outcome_ids: List[Tuple[int, int, int]]
    co_outcome_ids: List[Tuple[int, int, int]]
    np_outcome_ids: List[Tuple[int, int, int]]


class Outcomes(BaseModel):
    di_outcome_dtos: List[DichotomousOutcome]
    co_outcome_dtos: List[ContinuousOutcome]
    np_outcome_dtos: List[NonPoolableOutcome]
