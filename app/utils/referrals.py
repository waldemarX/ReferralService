from typing import Any
from app.models.token_db import Token


async def get_full_referral_tree(token: Token) -> dict[str | Any]:
    referral_list = await token.get_referral_tree_list(token.code)

    async def build_tree(referral_code):
        ref_data = next(
            (ref for ref in referral_list if ref[0] == referral_code), None
        )
        if not ref_data:
            return None
        invitees_number = [
            ref for ref in referral_list if ref[2] == ref_data[0]
        ]

        referral_data = {
            "code": ref_data[0],
            "identity": ref_data[1],
            "invitee_code": ref_data[2],
            "joined": ref_data[3],
            "invitees_number": len(invitees_number),
            "invited_users": [],
        }

        for referral in referral_list:
            if referral[2] == ref_data[0]:
                referral_data["invited_users"].append(
                    await build_tree(referral[0])
                )

        return referral_data

    return await build_tree(token.code)


async def get_referrals(token: Token) -> dict[str | Any]:
    referral_list = await token.get_referral_list(token.code)

    referral_data = {
        "code": token.code,
        "identity": token.identity,
        "invitee_code": token.invitee_code,
        "joined": token.joined,
        "invitees_number": len(referral_list),
        "invited_users": [],
    }

    for referral in referral_list:
        referral_data["invited_users"].append(
            {
                "code": referral.code,
                "identity": referral.identity,
                "invitee_code": referral.invitee_code,
                "joined": referral.joined,
            }
        )

    return referral_data


async def get_referral_parents(token: Token) -> list[dict[str | Any]]:
    referral_data = await token.get_referral_parent_list(token.code)
    json_data = [
        {
            "code": item[0],
            "identity": item[1],
            "invitee_code": item[2],
            "joined": item[3],
        }
        for item in referral_data
    ]
    return json_data
