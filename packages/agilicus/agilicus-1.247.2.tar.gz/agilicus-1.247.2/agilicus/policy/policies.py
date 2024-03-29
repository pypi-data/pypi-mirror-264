from ..input_helpers import (
    get_org_from_input_or_ctx,
)

from .. import context

from agilicus import (
    LabelName,
    PolicyTemplateInstance,
    PolicyTemplateInstanceSpec,
    MFAPolicyTemplate,
)

from ..output.table import (
    format_table,
    spec_column,
    subtable,
    column,
)


class LabelAddInfo:
    def __init__(self, apiclient):
        super().__init__()
        self.create_fn = lambda obj: apiclient.rules_api.create_ruleset_label(obj)
        # Can't replace. Just return the object
        self.replace_fn = lambda guid, obj: obj
        self.name_getter = lambda obj: obj.spec.name
        self.guid_finder = lambda obj_as_dict: obj_as_dict["spec"]["name"]


def set_multifactor_policy(ctx, name, duration, label=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    mfa = MFAPolicyTemplate(
        seconds_since_last_challenge=duration,
        labels=[LabelName(la) for la in (label or [])],
        template_type="mfa",
    )

    spec = PolicyTemplateInstanceSpec(
        org_id=org_id,
        name=name,
        template=mfa,
    )

    tmpl = PolicyTemplateInstance(spec=spec)
    return apiclient.policy_templates_api.create_policy_template_instance(tmpl)


def ruleset_labelled(ruleset, label):
    for ruleset_label in ruleset.spec.labels or []:
        if str(ruleset_label) == label:
            return True
    return False


def list_multifactor_policies(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    result = apiclient.policy_templates_api.list_policy_template_instances(org_id=org_id)
    return result.policy_template_instances


def format_multifactor_policies(ctx, templates):
    mfa_columns = [
        column("seconds_since_last_challenge"),
        column("labels"),
    ]
    mfa_table = subtable(ctx, "spec.template", mfa_columns)
    columns = [
        spec_column("org_id"),
        spec_column("name"),
        spec_column("template.template_type", "type"),
        mfa_table,
    ]

    return format_table(ctx, templates, columns)
