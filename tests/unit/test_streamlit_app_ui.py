import types

from backend.models.evidence import Evidence
from backend.models.problem import Problem, ProblemAnalysis
from backend.models.report import InnovationReport, Recommendation
import streamlit_app.app as app


class FakeContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def update(self, *args, **kwargs):
        return None

    def markdown(self, *args, **kwargs):
        return None

    def caption(self, *args, **kwargs):
        return None

    def metric(self, *args, **kwargs):
        return None

    def info(self, *args, **kwargs):
        return None

    def success(self, *args, **kwargs):
        return None

    def warning(self, *args, **kwargs):
        return None

    def write(self, *args, **kwargs):
        return None

    def dataframe(self, *args, **kwargs):
        return None

    def plotly_chart(self, *args, **kwargs):
        return None

    def download_button(self, *args, **kwargs):
        return None


class FakeState(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name, value):
        self[name] = value


class FakeStreamlit:
    def __init__(self):
        self.session_state = FakeState()
        self.sidebar = FakeContext()
        self._buttons = {}

    def set_page_config(self, *args, **kwargs):
        return None

    def markdown(self, *args, **kwargs):
        return None

    def caption(self, *args, **kwargs):
        return None

    def info(self, *args, **kwargs):
        return None

    def success(self, *args, **kwargs):
        return None

    def warning(self, *args, **kwargs):
        return None

    def write(self, *args, **kwargs):
        return None

    def plotly_chart(self, *args, **kwargs):
        return None

    def dataframe(self, *args, **kwargs):
        return None

    def download_button(self, *args, **kwargs):
        self._buttons["download"] = True
        return None

    def columns(self, spec):
        count = len(spec) if not isinstance(spec, int) else spec
        return [FakeContext() for _ in range(count)]

    def radio(self, label, options, index=0, label_visibility=None):
        return options[index]

    def button(self, *args, **kwargs):
        return kwargs.get("return_value", False)

    def status(self, *args, **kwargs):
        return FakeContext()

    def expander(self, *args, **kwargs):
        return FakeContext()

    def tabs(self, categories):
        return [FakeContext() for _ in categories]

    def form(self, *args, **kwargs):
        return FakeContext()

    def form_submit_button(self, *args, **kwargs):
        return False


def make_fake_report():
    analysis = ProblemAnalysis(
        title="Sample Analysis",
        summary="This is a sample summary.",
        keywords=("innovation", "policy"),
        challenges=("challenge one",),
        objectives=("objective one",),
        readiness_score=70,
        urgency_score=40,
    )
    evidence = (
        Evidence(
            id="e1",
            title="Test evidence",
            summary="A short summary.",
            category="Case Study",
            source="Local dataset",
            location="Hyderabad",
            relevance=0.82,
            tags=("innovation",),
            metadata={},
        ),
    )
    recommendations = (
        Recommendation(
            title="Pilot program",
            category="Program",
            rationale="This is a rationale.",
            action_steps=("Step 1", "Step 2"),
            confidence=0.75,
            impact_score=80,
            innovation_score=70,
            estimated_cost="INR 50 lakh",
            timeframe="6-12 months",
        ),
    )
    return InnovationReport(
        report_id="RPT-0001",
        created_at="2026-06-11T00:00:00Z",
        problem=Problem(text="Test problem."),
        title="Sample report",
        summary="Summary text.",
        analysis=analysis,
        recommendations=recommendations,
        evidence=evidence,
        policy_recommendations=("Policy 1",),
        dataset_version="hackathon-v1",
    )


def test_initialize_sets_session_state(monkeypatch):
    fake_st = FakeStreamlit()
    monkeypatch.setattr(app, "st", fake_st)
    app.initialize()
    assert fake_st.session_state["page"] == "Dashboard"
    assert fake_st.session_state["report"] is None


def test_hero_renders_markdown(monkeypatch):
    fake_st = FakeStreamlit()
    captured = {}

    def capture_markdown(text, unsafe_allow_html=False):
        captured["text"] = text
        captured["unsafe"] = unsafe_allow_html

    fake_st.markdown = capture_markdown
    monkeypatch.setattr(app, "st", fake_st)
    app.hero("TEST", "Title", "Description")
    assert "TEST" in captured["text"]
    assert captured["unsafe"] is True


def test_sidebar_assigns_selected_page(monkeypatch):
    fake_st = FakeStreamlit()
    fake_st.session_state["page"] = "Dashboard"
    monkeypatch.setattr(app, "st", fake_st)
    monkeypatch.setattr(
        app, "ReportRepository", lambda: types.SimpleNamespace(history=lambda: [])
    )
    app.sidebar()
    assert fake_st.session_state["page"] == "Dashboard"


def test_render_dashboard_calls_repository_and_renders(monkeypatch):
    fake_st = FakeStreamlit()
    fake_st.session_state["page"] = "Dashboard"
    monkeypatch.setattr(app, "st", fake_st)
    monkeypatch.setattr(
        app,
        "DatasetRepository",
        lambda: types.SimpleNamespace(
            counts=lambda: {"case_studies": 2, "research_papers": 1}
        ),
    )
    monkeypatch.setattr(
        app,
        "ReportRepository",
        lambda: types.SimpleNamespace(
            history=lambda: [{"impact_score": 60}, {"impact_score": 80}]
        ),
    )
    app.render_dashboard()


def test_render_upload_sets_report_after_analysis(monkeypatch):
    fake_st = FakeStreamlit()
    fake_st.session_state["page"] = "Upload Problem"
    fake_st.form_submit_button = lambda *args, **kwargs: False
    monkeypatch.setattr(app, "st", fake_st)
    monkeypatch.setattr(
        app,
        "render_problem_form",
        lambda: Problem(
            text="A" * 40,
            location="Hyderabad",
            sector="Transport",
            budget="INR 10-50 lakh",
            timeframe="3-6 months",
            target_population="commuters",
        ),
    )
    fake_report = make_fake_report()
    monkeypatch.setattr(
        app,
        "AnalysisOrchestrator",
        lambda: types.SimpleNamespace(run=lambda problem: fake_report),
    )
    app.render_upload()
    assert fake_st.session_state["report"] == fake_report


def test_require_report_warns_when_missing(monkeypatch):
    fake_st = FakeStreamlit()
    fake_st.session_state.clear()
    called = {"warning": False}

    def warn(*args, **kwargs):
        called["warning"] = True

    fake_st.warning = warn
    monkeypatch.setattr(app, "st", fake_st)
    result = app.require_report()
    assert result is None
    assert called["warning"] is True


def test_render_analysis_with_report(monkeypatch):
    fake_st = FakeStreamlit()
    fake_st.session_state["page"] = "AI Analysis"
    fake_st.session_state["report"] = make_fake_report()
    monkeypatch.setattr(app, "st", fake_st)
    app.render_analysis()


def test_render_recommendations_with_report(monkeypatch):
    fake_st = FakeStreamlit()
    fake_report = make_fake_report()
    fake_st.session_state["report"] = fake_report
    monkeypatch.setattr(app, "st", fake_st)
    monkeypatch.setattr(app, "score_chart", lambda report: None)
    app.render_recommendations()


def test_render_download_with_report(monkeypatch):
    fake_st = FakeStreamlit()
    fake_st.session_state["page"] = "Download Report"
    monkeypatch.setattr(app, "st", fake_st)
    fake_report = make_fake_report()
    fake_st.session_state["report"] = fake_report
    monkeypatch.setattr(app, "generate_markdown", lambda report: "# Report")
    monkeypatch.setattr(app, "evidence_frame", lambda report: None)
    app.render_download()
    assert fake_st._buttons.get("download", False)


def test_report_view_helpers():
    fake_report = make_fake_report()
    figure = app.score_chart(fake_report)
    frame = app.evidence_frame(fake_report)
    assert figure is not None
    assert "Evidence" in frame.columns
