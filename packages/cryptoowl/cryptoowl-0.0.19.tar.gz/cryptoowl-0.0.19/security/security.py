import json

import requests

from common.secretmanager import SecretManager
from configs import write_db
from security.constants import HONEYPOT_FINDER_URL, GO_PLUS_URL, INSERT_OR_UPDATE_ETH_SECURITY_DATA_QUERY, \
    UPDATE_OTHER_CHAIN_SECURITY_DATA_QUERY, ID_TO_CHAIN_MAP, GET_QUICK_AUDIT_URL, QUICK_INTEL_API_KEY_SECRET_ID, \
    UPDATE_OTHER_CHAIN_SECURITY_DATA_FROM_QUICK_INTEL_QUERY


class Honeypot:
    def __init__(self):
        self.__aws_secret_manager = SecretManager()
        self.__api_key_values = self.__aws_secret_manager.get_secret_key_value(
            secret_name=QUICK_INTEL_API_KEY_SECRET_ID)
        self.__api_key = self.__api_key_values.get("api-key")

    @classmethod
    def __store_security_date(cls, security_data, chain_id, from_qi=False):
        if security_data:
            token_id = security_data.get("token_id")
            honeypot = security_data.get("honeypot")
            buy_tax = security_data.get("buy_tax")
            sell_tax = security_data.get("sell_tax")
            holder_count = security_data.get("holder_count")
            lp_burned = security_data.get("lp_burned")
            is_scam = security_data.get("is_scam")
            can_burn = security_data.get("can_burn")
            can_mint = security_data.get("can_mint")
            can_freeze = security_data.get("can_freeze")

            if chain_id == 1:
                value = (token_id, honeypot, sell_tax, buy_tax)
                query = INSERT_OR_UPDATE_ETH_SECURITY_DATA_QUERY
            else:
                if from_qi:
                    value = (honeypot, sell_tax, buy_tax, lp_burned, is_scam, can_burn, can_mint, can_freeze, token_id)
                    query = UPDATE_OTHER_CHAIN_SECURITY_DATA_FROM_QUICK_INTEL_QUERY
                else:
                    value = (honeypot, sell_tax, buy_tax, holder_count, token_id)
                    query = UPDATE_OTHER_CHAIN_SECURITY_DATA_QUERY

            try:
                write_db.execute_query(query=query, values=value)
                print(f"INFO: Data updated for: {token_id}")
            except Exception as error:
                print(f"ERROR: {error}")

    def get_security_data(self, chain_id, token_id):
        if chain_id == 1:
            security_data_dict = self.get_data_from_honeypot(chain_id=chain_id, token_id=token_id)
            if security_data_dict.get("buy_tax") is None or security_data_dict.get("sell_tax") is None:
                return self.security_data_dict_for_non_eth(chain_id, token_id)
            else:
                return security_data_dict
        else:
            return self.security_data_dict_for_non_eth(chain_id, token_id)

    def security_data_dict_for_non_eth(self, chain_id, token_id):
        security_data_dict = self.get_data_from_goplus(chain_id, token_id)
        if security_data_dict.get("buy_tax") is None or security_data_dict.get("sell_tax") is None:
            security_data_dict = self.get_data_from_quickintel(chain_id, token_id)
            return security_data_dict
        return security_data_dict

    @classmethod
    def get_data_from_goplus(cls, chain_id, token_id):
        token_id = token_id.lower()
        url = GO_PLUS_URL.format(chain_id=chain_id, token_id=token_id)
        response = requests.get(url=url)
        try:
            if response.status_code not in [500, 404]:
                result = response.json().get("result")
                if result:
                    is_honey_pot = result.get(token_id).get('is_honeypot')
                    buy_tax = result.get(token_id).get('buy_tax')
                    sell_tax = result.get(token_id).get('sell_tax')
                    holders_count = result.get(token_id).get("holder_count")
                    security_data = {"honeypot": is_honey_pot, "buy_tax": buy_tax, "sell_tax": sell_tax,
                                     "holder_count": holders_count, "token_id": token_id}
                    cls.__store_security_date(security_data=security_data, chain_id=chain_id)
                    return security_data
        except Exception as error:
            print(f"ERROR: In get_data_from_goplus {error}")
        return {}

    @classmethod
    def get_data_from_honeypot(cls, chain_id, token_id):
        url = HONEYPOT_FINDER_URL.format(token_id=token_id)
        response = requests.get(url=url)
        try:
            if response.status_code not in [500, 404]:
                data = response.json()
                is_honey_pot = data.get('IsHoneypot')
                buy_tax = round(data.get('BuyTax'))
                sell_tax = round(data.get('SellTax'))
                security_data = {"honeypot": is_honey_pot, "buy_tax": buy_tax, "sell_tax": sell_tax,
                                 "token_id": token_id}
                cls.__store_security_date(security_data=security_data, chain_id=chain_id)
                return security_data
        except Exception as error:
            print(f"ERROR: In get_data_from_honeypot {error}")

    def get_data_from_quickintel(self, chain_id, token_id):
        chain = ID_TO_CHAIN_MAP.get(chain_id)
        url = GET_QUICK_AUDIT_URL
        payload = {"chain": chain, "tokenAddress": token_id}
        headers = {"X-QKNTL-KEY": self.__api_key, "Content-Type": "application/json"}
        response = requests.post(url=url, data=json.dumps(payload), headers=headers)
        try:
            if response.status_code not in [500, 404]:
                data = response.json()
                token_dynamic_details = data.get("tokenDynamicDetails", {})
                quick_audit = data.get("quickiAudit", {})
                honeypot = token_dynamic_details.get("is_Honeypot")
                buy_tax = token_dynamic_details.get("buy_Tax")
                sell_tax = token_dynamic_details.get("sell_Tax")
                lp_burned = token_dynamic_details.get("lp_Burned")
                is_scam = data.get("isScam")
                can_burn = quick_audit.get("can_Burn")
                can_mint = quick_audit.get("can_Mint")
                can_freeze = quick_audit.get("can_Freeze_Trading")
                security_data = {"honeypot": honeypot, "buy_tax": buy_tax, "sell_tax": sell_tax, "lp_burned": lp_burned,
                                 "is_scam": is_scam, "can_burn": can_burn, "can_mint": can_mint,
                                 "can_freeze": can_freeze, "token_id": token_id}
                self.__store_security_date(security_data=security_data, chain_id=chain_id, from_qi=True)
                return security_data

        except Exception as error:
            print(f"ERROR: In get_data_from_quickintel {error}")
