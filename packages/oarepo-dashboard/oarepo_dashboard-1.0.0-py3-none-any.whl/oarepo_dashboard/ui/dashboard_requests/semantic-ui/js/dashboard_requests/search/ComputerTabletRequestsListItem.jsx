// This file is part of InvenioRDM
// Copyright (C) 2023 CERN.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { i18next } from "@translations/oarepo_dashboard";
import { default as RequestTypeIcon } from "@js/invenio_requests/components/RequestTypeIcon";
import React from "react";
import RequestTypeLabel from "@js/invenio_requests/request/RequestTypeLabel";
import RequestStatusLabel from "@js/invenio_requests/request/RequestStatusLabel";
import { Icon, Item } from "semantic-ui-react";
import PropTypes from "prop-types";
import { toRelativeTime } from "react-invenio-forms";
import { DateTime } from "luxon";

export const ComputerTabletRequestsListItem = ({
  result,
  updateQueryState,
  currentQueryState,
  detailsURL,
}) => {
  const createdDate = new Date(result.created);
  let creatorName = "";
  const isCreatorUser = "user" in result.created_by;
  const isCreatorCommunity = "community" in result.created_by;
  const isCreatorGuest = "email" in result.created_by;
  if (isCreatorUser) {
    creatorName =
      result.expanded?.created_by.profile?.full_name ||
      result.expanded?.created_by.username ||
      result.created_by.user;
  } else if (isCreatorCommunity) {
    creatorName =
      result.expanded?.created_by.metadata?.title ||
      result.created_by.community;
  } else if (isCreatorGuest) {
    creatorName = result.created_by.email;
  }

  const getUserIcon = (receiver) => {
    return receiver?.is_ghost ? "user secret" : "users";
  };
  const relativeTime = toRelativeTime(
    createdDate.toISOString(),
    i18next.language
  );
  return (
    <Item
      key={result.id}
      className="computer tablet only rel-p-1 rel-mb-1 result-list-item request"
    >
      <div className="status-icon mr-10">
        <Item.Content verticalAlign="top">
          <Item.Extra>
            <RequestTypeIcon type={result.type} />
          </Item.Extra>
        </Item.Content>
      </div>
      <Item.Content>
        <Item.Extra>
          {result.type && <RequestTypeLabel type={result.type} />}
          {result.status && result.is_closed && (
            <RequestStatusLabel status={result.status} />
          )}
        </Item.Extra>
        <Item.Header className="truncate-lines-2  mt-5">
          <a className="header-link" href={detailsURL}>
            {result.title}
          </a>
        </Item.Header>
        <Item.Meta>
          <small>
            {i18next.t("Opened by", { relativeTime: relativeTime })}{" "}
            {creatorName}
          </small>
          <small className="right floated">
            {result.receiver?.community &&
              result.expanded?.receiver.metadata.title && (
                <>
                  <Icon
                    className="default-margin"
                    name={getUserIcon(result.expanded?.receiver)}
                  />
                  <span className="ml-5">
                    {result.expanded?.receiver.metadata.title}
                  </span>
                </>
              )}
            {result.expires_at && (
              <span>
                {i18next.t("Expires at: {{- expiringDate}}", {
                  expiringDate: DateTime.fromISO(
                    result.expires_at
                  ).toLocaleString(i18next.language),
                })}
              </span>
            )}
          </small>
        </Item.Meta>
      </Item.Content>
    </Item>
  );
};

ComputerTabletRequestsListItem.propTypes = {
  result: PropTypes.object.isRequired,
  updateQueryState: PropTypes.func.isRequired,
  currentQueryState: PropTypes.object.isRequired,
  detailsURL: PropTypes.string.isRequired,
};
