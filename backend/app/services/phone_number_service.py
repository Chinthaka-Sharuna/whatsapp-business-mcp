from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session
import logging

from utils.request_maker import RequestMaker
from config import Config

from models.schemas.phone_number import PhoneNumberAdminResponse
from dependencies.type import DBSession

from models.entity.phone_numbers import PhoneNumbers



class PhoneNumberService:

    @staticmethod
    def add_new_number():
        pass

    @staticmethod
    async def sync_phone_numbers(session: Session = Depends(DBSession),) -> list[PhoneNumberAdminResponse]:

        logging.info("Syncing phone numbers...")
        data = await RequestMaker.request(
            method='GET',
            url=f"{Config.BASE_URL}/{Config.WABA_ID}/phone_numbers",
            headers={
                "Authorization": f"Bearer {Config.ACCESS_TOKEN}"
                }
        )
        for item in data["data"]:
            added = []
            target_number = session.get(PhoneNumbers,item["id"])
            if not target_number:
                new_phone_number = PhoneNumbers(
                    wapn_id=item["id"],
                    wa_number=item["display_phone_number"],
                    label="sales"
                )
                session.add(new_phone_number)
                added.append(item["display_phone_number"])

        session.commit()
        logging.info(f"Added {len(added)} new phone numbers.")

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": f"Added {len(added)} new number"
            }
        )