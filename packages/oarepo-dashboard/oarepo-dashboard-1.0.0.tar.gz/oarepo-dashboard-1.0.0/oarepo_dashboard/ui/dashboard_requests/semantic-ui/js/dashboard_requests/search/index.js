import React from "react";
import { Grid } from "semantic-ui-react";
import { parametrize } from "react-overridable";
import {
  createSearchAppsInit,
  parseSearchAppConfigs,
  SearchappSearchbarElement,
} from "@js/oarepo_ui";
import { withState } from "react-searchkit";
import { RequestsEmptyResultsWithState } from "@js/invenio_requests/search";
import { defaultContribComponents } from "@js/invenio_requests/contrib";
import { PropTypes } from "prop-types";
import {
  UserDashboardSearchAppLayoutHOC,
  UserDashboardSearchAppResultView,
  FacetsButtonGroup,
} from "@js/dashboard_components";
import { i18next } from "@translations/oarepo_dashboard";
import { ComputerTabletRequestsListItem } from "./ComputerTabletRequestsListItem";
import { MobileRequestsListItem } from "./MobileRequestsListItem";
import { requestTypeSpecificComponents } from "./RequestTypeSpecificComponents";

const [{ overridableIdPrefix }] = parseSearchAppConfigs();

export function RequestsResultsItemTemplateDashboard({ result }) {
  const ComputerTabletRequestsItemWithState = withState(
    ComputerTabletRequestsListItem
  );
  const MobileRequestsItemWithState = withState(MobileRequestsListItem);
  const detailPageUrl = `/docs/${result?.topic?.documents}`;
  return (
    <>
      <ComputerTabletRequestsItemWithState
        result={result}
        detailsURL={detailPageUrl}
      />
      <MobileRequestsItemWithState result={result} detailsURL={detailPageUrl} />
    </>
  );
}

RequestsResultsItemTemplateDashboard.propTypes = {
  result: PropTypes.object.isRequired,
};
// TODO: currently there is no API to determine if request is mine or not
export const FacetButtons = () => (
  <React.Fragment>
    <Grid.Column only="computer" textAlign="right">
      <FacetsButtonGroup facetName="is_open" />
      {/* <span className="rel-ml-2"></span> */}
      {/* <FacetsButtonGroup
        facetName="is_mine"
        trueButtonText={i18next.t("My")}
        falseButtonText={i18next.t("Others")}
      /> */}
    </Grid.Column>
    <Grid.Column only="mobile tablet" textAlign="left">
      <FacetsButtonGroup facetName="is_open" />
    </Grid.Column>
    {/* <Grid.Column only="mobile tablet" textAlign="right">
      <FacetsButtonGroup
        facetName="is_mine"
        trueButtonText={i18next.t("My")}
        falseButtonText={i18next.t("Others")}
      />
    </Grid.Column> */}
  </React.Fragment>
);

const UserDashboardSearchAppResultViewWAppName = parametrize(
  UserDashboardSearchAppResultView,
  {
    appName: overridableIdPrefix,
  }
);

export const DashboardUploadsSearchLayout = UserDashboardSearchAppLayoutHOC({
  placeholder: i18next.t("Search in my requests..."),
  extraContent: FacetButtons,
  appName: overridableIdPrefix,
});
export const componentOverrides = {
  [`${overridableIdPrefix}.EmptyResults.element`]:
    RequestsEmptyResultsWithState,
  [`${overridableIdPrefix}.ResultsList.item`]:
    RequestsResultsItemTemplateDashboard,
  [`${overridableIdPrefix}.SearchApp.results`]:
    UserDashboardSearchAppResultViewWAppName,
  [`${overridableIdPrefix}.SearchBar.element`]: SearchappSearchbarElement,
  [`${overridableIdPrefix}.SearchApp.layout`]: DashboardUploadsSearchLayout,
  // from invenio requests in case we have some overlapping request types
  ...defaultContribComponents,
  // our request type specific components (icons, labels, etc.)
  ...requestTypeSpecificComponents,
};

createSearchAppsInit({ componentOverrides });
