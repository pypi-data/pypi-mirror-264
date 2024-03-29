import React, { useContext } from "react";
import PropTypes from "prop-types";
import { i18next } from "@translations/oarepo_dashboard";
import { Button } from "semantic-ui-react";
import { withState } from "react-searchkit";
import { SearchConfigurationContext } from "@js/invenio_search_ui/components";

const FacetsButtonGroupNameTogglerComponent = ({
  currentResultsState,
  currentQueryState,
  updateQueryState,
  facetNames,
  firstFacetButtonText,
  secondFacetButtonText,
  keepFiltersOnUpdate,
  ...uiProps
}) => {
  const { initialQueryState } = useContext(SearchConfigurationContext);
  const currentFilter = currentQueryState.filters?.find((f) =>
    facetNames.includes(f[0])
  );
  const initialQueryFacets = initialQueryState.filters?.map((f) => f[0]);
  if (!currentFilter)
    console.error(
      "FacetsButtonGroup: Query does not contain any of the facets you wish to toggle between, please make sure you are passing initialFilters properly"
    );
  const facetStatus = currentFilter && JSON.parse(currentFilter?.[1]);
  const handleFacetNameChange = (facetName) => {
    if (currentFilter[0] === facetName) return;

    currentQueryState.filters = keepFiltersOnUpdate
      ? currentQueryState.filters.filter(
          (element) => element[0] !== currentFilter[0]
        )
      : [
          ...(currentQueryState?.filters
            ? currentQueryState.filters.filter((element) =>
                initialQueryFacets.includes(element[0])
              )
            : []),
        ];
    currentQueryState.filters = currentQueryState.filters.filter(
      (f) => !facetNames.includes(f[0])
    );

    currentQueryState.filters.push([facetName, facetStatus]);
    updateQueryState(currentQueryState);
  };
  return (
    <Button.Group size="mini" className="rel-mb-1" {...uiProps}>
      <Button
        onClick={() => handleFacetNameChange(facetNames[0])}
        className="request-search-filter"
        active={facetNames[0] === currentFilter[0]}
      >
        {firstFacetButtonText}
      </Button>
      <Button
        onClick={() => handleFacetNameChange(facetNames[1])}
        className="request-search-filter"
        active={facetNames[1] === currentFilter[0]}
      >
        {secondFacetButtonText}
      </Button>
    </Button.Group>
  );
};

FacetsButtonGroupNameTogglerComponent.propTypes = {
  currentQueryState: PropTypes.object.isRequired,
  updateQueryState: PropTypes.func.isRequired,
  currentResultsState: PropTypes.object.isRequired,
  facetNames: PropTypes.array.isRequired,
  firstFacetButtonText: PropTypes.string,
  secondFacetButtonText: PropTypes.string,
  keepFiltersOnUpdate: PropTypes.bool,
};
FacetsButtonGroupNameTogglerComponent.defaultProps = {
  firstFacetButtonText: i18next.t("My"),
  secondFacetButtonText: i18next.t("Others"),
  keepFiltersOnUpdate: true,
};
export const FacetsButtonGroupNameToggler = withState(
  FacetsButtonGroupNameTogglerComponent
);
