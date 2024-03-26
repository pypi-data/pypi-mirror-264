"""Add Fastmail DNS records to a Porkbun domain."""

import dataclasses
import json
import os
import typing

import requests

Wildcard = typing.Literal["*"]
RecordType = typing.Literal[
    "A",
    "MX",
    "CNAME",
    "ALIAS",
    "TXT",
    "NA",
    "AAAA",
    "SRV",
    "TLSA",
    "CAA",
]


@dataclasses.dataclass
class Record:
    """
    :param type: The type of record being created.
    :param host: The subdomain for the record being created, not including the domain itself.
        Leave blank to create a record on the root domain.
        Use * to create a wildcard record.
    :param answer: The answer content for the record.
        Please see the DNS management popup from the domain management console for proper formatting of each record type.
    :param ttl: The time to live in seconds for the record.
        The minimum and the default is 600 seconds.
    :param priority: The priority of the record for those that support it.
    :param notes: Notes for the record.
    """

    type: RecordType
    host: str
    answer: str = ""
    ttl: int = 600
    priority: int | None = None
    notes: str | None = None


class PorkbunService:
    ROOT_URL = "https://porkbun.com/api/json/v3"

    def __init__(
        self,
        secret_api_key: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.secret_api_key = secret_api_key or os.environ["PORKBUN_SECRET_API_KEY"]
        self.api_key = api_key or os.environ["PORKBUN_API_KEY"]

    def _request(self, relative_url: str, data: dict) -> dict[str, typing.Any]:
        data.setdefault("secretapikey", self.secret_api_key)
        data.setdefault("apikey", self.api_key)
        json_data = json.dumps(data)
        url = self.ROOT_URL + relative_url
        response = requests.post(url, data=json_data, timeout=5.0)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise requests.exceptions.HTTPError(
                "Did you make sure to enable API access for this domain in the Porkbun admin?"
            ) from error

        response_data = response.json()
        if response_data["status"].casefold() != "success":
            raise ValueError(response_data)
        return response_data

    def add_record(
        self,
        domain: str,
        record: Record,
    ) -> str:
        """
        Add a DNS record to the domain.

        :returns: The ID of the record created.
        """
        data = {
            "type": record.type,
            "content": record.answer,
            "ttl": record.ttl,
        }
        if record.host:
            data["name"] = record.host
        if record.priority:
            data["prio"] = record.priority

        response_data = self._request(f"/dns/create/{domain}", data)
        created_record_id = response_data["id"]
        return created_record_id


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="The domain to add Fastmail DNS records to")
    args = parser.parse_args()
    domain: str = args.domain

    FASTMAIL_MX_RECORD_1 = Record(
        "MX",
        "",
        "in1-smtp.messagingengine.com",
        priority=10,
        notes="Fastmail",
    )
    FASTMAIL_MX_RECORD_2 = Record(
        "MX",
        "",
        "in2-smtp.messagingengine.com",
        priority=20,
        notes="Fastmail",
    )

    FASTMAIL_CNAME_DKIM_RECORD_1 = Record(
        "CNAME",
        "fm1._domainkey",
        f"fm1.{domain}.dkim.fmhosted.com",
        notes="Fastmail",
    )
    FASTMAIL_CNAME_DKIM_RECORD_2 = Record(
        "CNAME",
        "fm2._domainkey",
        f"fm2.{domain}.dkim.fmhosted.com",
        notes="Fastmail",
    )
    FASTMAIL_CNAME_DKIM_RECORD_3 = Record(
        "CNAME",
        "fm3._domainkey",
        f"fm3.{domain}.dkim.fmhosted.com",
        notes="Fastmail",
    )

    FASTMAIL_TXT_SPF_RECORD = Record(
        "TXT",
        "",
        "v=spf1 include:spf.messagingengine.com ?all",
        notes="Fastmail",
    )

    FASTMAIL_RECORDS = (
        FASTMAIL_MX_RECORD_1,
        FASTMAIL_MX_RECORD_2,
        FASTMAIL_CNAME_DKIM_RECORD_1,
        FASTMAIL_CNAME_DKIM_RECORD_2,
        FASTMAIL_CNAME_DKIM_RECORD_3,
        FASTMAIL_TXT_SPF_RECORD,
    )

    service = PorkbunService()
    for record in FASTMAIL_RECORDS:
        record_id = service.add_record(domain, record)
        print(f"New record ID: {record_id}")


if __name__ == "__main__":
    main()
