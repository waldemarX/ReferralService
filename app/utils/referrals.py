from app.models.token_db import Token


async def get_full_referral_tree(token):
    async def build_referral_tree(token):
        referral_list = await Token.get_referrals(token.code)

        invited_number_all = len(referral_list)

        referral_data = {
            "code": token.code,
            "identity": token.identity,
            "joined": token.joined,
            "invitee_code": token.invitee_code,
            "invited_number": len(referral_list),
            "invited_users": [],
        }

        for referral in referral_list:
            child_data, child_invited_number_all = await build_referral_tree(
                referral
            )
            invited_number_all += child_invited_number_all
            referral_data["invited_users"].append(child_data)

        return referral_data, invited_number_all

    data, invited_number_all = await build_referral_tree(token)
    data["invited_number_all"] = invited_number_all

    return data


async def get_list_of_referrals(token):
    referral_list = await Token.get_referrals(token.code)

    referral_data = {
        "code": token.code,
        "identity": token.identity,
        "joined": token.joined,
        "invitee_code": token.invitee_code,
        "invited_number": len(referral_list),
        "invited_users": [],
    }

    for referral in referral_list:
        referral_data["invited_users"].append(
            {
                "code": referral.code,
                "identity": referral.identity,
                "joined": referral.joined,
                "invitee_code": referral.invitee_code,
            }
        )

    return referral_data


async def get_referral_parents_tree(token):
    async def build_referral_tree(token):
        parent = await Token.find_first_by_id(token.invitee_code)

        referral_data = {
            "code": token.code,
            "identity": token.identity,
            "joined": token.joined,
            "invitee_code": token.invitee_code,
            "invited_by": [],
        }

        if parent is not None:
            parent_data = await build_referral_tree(parent)
            referral_data["invited_by"].append(parent_data)

        return referral_data

    data = await build_referral_tree(token)

    return data
