from datetime import datetime as dt

from src.domain.value.filed import userStatusFiled, completedFiled, qtyFiled, quoteQtyFiled, assetQtyFiled, trasactionIdFile
from src.application.dto.users_dto import user_hisotry_output, HistoryDto

class UserHistoryDomainService:

    @staticmethod
    def build_history_res(side_type, trans_type, asset, qty):
        dlist = []
        for side_doc in side_type:
            side_output_doc = user_hisotry_output(trans_type, side_doc, asset, qty)
            if qty == qtyFiled:
                side_output_doc[qtyFiled] = float(side_doc.to_dict()[qtyFiled])
                side_output_doc[quoteQtyFiled] = 0
            elif qty == assetQtyFiled:
                side_output_doc[quoteQtyFiled] = 0
                side_output_doc[userStatusFiled] = side_doc.to_dict()[userStatusFiled]
                if side_output_doc[userStatusFiled] == completedFiled:
                    side_output_doc[trasactionIdFile] = side_doc.to_dict()[trasactionIdFile]
            else:
                side_output_doc[quoteQtyFiled] = side_doc.to_dict()[quoteQtyFiled]
            dlist.append(side_output_doc)
        return dlist