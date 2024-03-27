from ..input_helpers import (
    get_org_from_input_or_ctx,
)

from .. import context
from ..rules.rules import (
    add_list_resources_sdk,
    list_rules,
    list_rule_trees,
    list_rulesets,
    RuleAddInfo,
    RulesetAddInfo,
    RuleTreeAddInfo,
)

from ..output.table import (
    format_table,
    column,
)

from .templates import MultifactorTemplate, MFA_LABEL


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
    tmpl = MultifactorTemplate(name, duration, org_id=org_id, labels=label)

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    add_list_resources_sdk(
        ctx,
        tmpl.get_rules(),
        RuleAddInfo(apiclient),
        handle_failure=False,
    )
    add_list_resources_sdk(
        ctx, tmpl.get_trees(), RuleTreeAddInfo(apiclient), handle_failure=False
    )
    add_list_resources_sdk(
        ctx, tmpl.get_labels(), LabelAddInfo(apiclient), handle_failure=False
    )

    add_list_resources_sdk(
        ctx, tmpl.get_sets(), RulesetAddInfo(apiclient), handle_failure=False
    )

    return tmpl


def ruleset_labelled(ruleset, label):
    for ruleset_label in ruleset.spec.labels or []:
        if str(ruleset_label) == label:
            return True
    return False


def list_multifactor_policies(ctx, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    rules = list_rules(ctx, org_id=org_id)
    trees = list_rule_trees(ctx, org_id=org_id)
    sets = list_rulesets(ctx, org_id=org_id)

    names = []
    for ruleset in sets:
        if ruleset_labelled(ruleset, MFA_LABEL):
            names.append(str(ruleset.spec.name))

    templates = []
    for name in names:
        tmpl = MultifactorTemplate.from_api(
            name=name, rules=rules, trees=trees, sets=sets, org_id=org_id
        )
        if tmpl:
            templates.append(tmpl)

    return templates


def format_multifactor_policies(ctx, templates):
    columns = [
        column("name"),
        column("org_id"),
        column("duration"),
        column("labels"),
    ]

    return format_table(ctx, templates, columns)
