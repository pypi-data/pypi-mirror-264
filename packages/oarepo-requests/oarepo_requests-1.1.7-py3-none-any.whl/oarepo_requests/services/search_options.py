from invenio_records_resources.services.records.params import FilterParam
from invenio_requests.resources.requests.config import RequestSearchRequestArgsSchema, RequestsResourceConfig
from invenio_requests.services.requests.config import RequestSearchOptions, RequestsServiceConfig
from marshmallow import fields
from opensearch_dsl.query import Bool, Term


class RequestOwnerFilterParam(FilterParam):
    def apply(self, identity, search, params):
        value = params.pop(self.param_name, None)
        if value is not None:
            search = search.filter("term", **{self.field_name: identity.id})
        return search


class RequestReceiverFilterParam(FilterParam):
    def apply(self, identity, search, params):
        value = params.pop(self.param_name, None)
        my_groups = [
            n.value for n in identity.provides if n.method == 'role'
        ]
        if value is not None:
            search = search.filter(Bool(should=[
                # explicitly myself
                Term(**{f"{self.field_name}.user": identity.id}),
                # my roles
                *[
                    Term(**{f"{self.field_name}.group": group_id}) for group_id in my_groups
                ],
                # TODO: add my communities where I have a role to accept requests
            ], minimum_should_match=1))
        return search


class EnhancedRequestSearchOptions(RequestSearchOptions):
    params_interpreters_cls = RequestSearchOptions.params_interpreters_cls + [
        RequestOwnerFilterParam.factory("mine", "created_by.user"),
        RequestReceiverFilterParam.factory("assigned", "receiver")
    ]


class ExtendedRequestSearchRequestArgsSchema(RequestSearchRequestArgsSchema):
    mine = fields.Boolean()
    assigned = fields.Boolean()


def override_invenio_request_search_options(*args, **kwargs):
    # this monkey patch should be done better
    RequestsServiceConfig.search = EnhancedRequestSearchOptions
    RequestsResourceConfig.request_search_args = ExtendedRequestSearchRequestArgsSchema