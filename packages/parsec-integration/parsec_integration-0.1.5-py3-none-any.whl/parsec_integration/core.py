from datetime import datetime
from random import randint

from zeep import xsd

from parsec_integration.dto.dto import ParsecConfigDto, ParsecSystemInfo, OrgUnit, Person, \
    VisitorRequest, Guid, \
    ClaimStatus, Identifier, BasePerson, BaseOrgUnit
from parsec_integration.errors import ParsecIntegrationError
from parsec_integration.main import Parsec


class ParsecCore:

    async def init(self, config: ParsecConfigDto, locale=False):
        self.system_info: ParsecSystemInfo = ParsecSystemInfo()
        self.config = config
        self.core = Parsec(f"http://{self.config.host}:{self.config.port}"
                           f"/IntegrationService/IntegrationService.asmx?WSDL")
        self.session = None
        self.session_id = None
        await self._get_version()
        await self._get_domains()
        await self._open_session(locale)

    async def _get_version(self):
        self.system_info.version = self.core.get_version()

    async def _get_domains(self):
        self.system_info.domains = self.core.get_domains()

    async def _open_session(self, locale):
        if locale:
            result = (self.core.open_session(self.config.domain, self.config.login, self.config.password,
                                             self.config.language)).Value
            if not result:
                raise Exception("OpenSessionWithInLocale error")
        r = self.core.open_session(self.config.domain, self.config.login, self.config.password)
        result = r.Value

        self.session = result
        self.session_id = self.session.SessionID

    # --------------------------Organization----------------------------------
    async def get_root_organization(self):
        return self.core.get_root_org_unit(self.session_id)

    async def get_all_organizations(self):
        root_org = await self.get_root_organization()
        return [org for org in self.core.get_org_units_hierarchy(self.session_id)
                if org.PARENT_ID == root_org.ID and org.NAME != "SYSTEM"]

    async def get_organization(self, organization_uuid: Guid):
        for org in self.core.get_org_units_hierarchy(self.session_id):
            if org.ID == organization_uuid:
                return org
        else:
            raise ParsecIntegrationError(f"Organization with uuid: {organization_uuid} not found")

    async def create_organization(self, organization_name: str):
        return self.core.create_org_unit(self.session_id,
                                         org_unit=OrgUnit.Create(
                                             NAME=organization_name,
                                             PARENT_ID=(await self.get_root_organization()).ID))

    async def update_organization(self, organization_name: str, organization_uuid: Guid):
        org = await self.get_organization(organization_uuid=organization_uuid)
        edit_session_id = (self.core.open_org_unit_editing_session(self.session_id, org.ID)).Value
        org.NAME = organization_name
        return self.core.save_org_unit(edit_session_id, org)

    async def delete_organization(self, organization_uuid: Guid):
        org = await self.get_organization(organization_uuid=organization_uuid)
        return self.core.delete_org_unit(self.session_id, org.ID)

    # ---------------------------Department-----------------------------------

    async def get_all_departments(self):
        root_org = await self.get_root_organization()
        return [org for org in self.core.get_org_units_hierarchy(self.session_id)
                if org.PARENT_ID != root_org.ID]

    async def get_department(self, department_uuid: str):
        for org in self.core.get_org_units_hierarchy(self.session_id):
            if org.ID == department_uuid:
                return org
        else:
            raise ParsecIntegrationError(f"Department with uuid: {department_uuid} not found")

    async def create_department(self, department_name: str, organization_uuid: Guid):
        parent_org = await self.get_organization(organization_uuid=organization_uuid)
        org_dto = OrgUnit.Create(NAME=department_name,
                                 PARENT_ID=parent_org.ID)
        return self.core.create_org_unit(self.session_id, org_dto)

    async def update_department(self, department_name: str, department_uuid: Guid):
        dep = await self.get_department(department_uuid=department_uuid)
        edit_session_id = (self.core.open_org_unit_editing_session(self.session_id, dep.ID)).Value
        dep.NAME = department_name
        return self.core.save_org_unit(edit_session_id, dep)

    async def delete_department(self, department_uuid: Guid):
        dep = await self.get_department(department_uuid=department_uuid)
        return self.core.delete_org_unit(self.session_id, dep.ID)

    # ---------------------------Employer--------------------------------------

    async def get_all_employers(self):
        return [employee for employee in self.core.get_org_units_hierarchy_with_persons(self.session_id)
                if hasattr(employee, "FIRST_NAME")]

    async def get_employer(self, employee_uuid: Guid):
        return self.core.get_person(self.session_id, person_id=employee_uuid)

    async def create_employer(self, dto: BasePerson.Create | Person.Create):
        await self.get_department(department_uuid=dto.ORG_ID)
        return self.core.create_person(self.session_id, dto)

    async def update_employer(self, dto: BasePerson.Update | Person.Update):
        emp = await self.get_employer(employee_uuid=dto.ID)
        if not emp:
            raise ParsecIntegrationError(f"Employee with uuid: {dto.ID} not found")
        edit_session = self.core.open_person_editing_session(self.session_id, dto.ID)
        if hasattr(dto, "ORG_ID"):
            object_type = self.core.client.get_type('ns0:Person')
            object_wrap = xsd.Element('Person', object_type)
            value = object_wrap(dto.ID,
                                dto.LAST_NAME if dto.LAST_NAME else emp.LAST_NAME,
                                dto.FIRST_NAME if dto.FIRST_NAME else emp.FIRST_NAME,
                                dto.MIDDLE_NAME if dto.MIDDLE_NAME else emp.MIDDLE_NAME,
                                dto.TAB_NUM if dto.TAB_NUM else emp.TAB_NUM,
                                dto.ORG_ID)
            return self.core.save_person(edit_session.Value, value)
        dto.LAST_NAME = dto.LAST_NAME if dto.LAST_NAME else emp.LAST_NAME
        dto.FIRST_NAME = dto.FIRST_NAME if dto.FIRST_NAME else emp.FIRST_NAME
        dto.MIDDLE_NAME = dto.MIDDLE_NAME if dto.MIDDLE_NAME else emp.MIDDLE_NAME
        dto.TAB_NUM = dto.TAB_NUM if dto.TAB_NUM else emp.TAB_NUM
        return self.core.save_person(edit_session.Value, dto)

    async def delete_employer(self, employee_uuid: Guid):
        return self.core.delete_person(self.session_id, employee_uuid)

    # ----------------------------Visitor--------------------------------------

    async def get_visitor(self, visitor_uuid: Guid):
        return self.core.get_person(self.session_id, person_id=visitor_uuid)

    async def create_visitor(self, dto: Person.Create):
        await self.get_department(department_uuid=dto.ORG_ID)
        return self.core.create_visitor(self.session_id, dto)

    async def update_visitor(self):
        pass

    async def delete_visitor(self, visitor_uuid: Guid):
        return self.core.delete_person(self.session_id, visitor_uuid)

    # ----------------------------Vehicle--------------------------------------

    async def get_vehicles(self, vehicle_uuid: Guid):
        return self.core.get_person(self.session_id, person_id=vehicle_uuid)

    async def create_vehicle(self, dto: Person.Create):
        await self.get_department(department_uuid=dto.ORG_ID)
        return self.core.create_vehicle(self.session_id, dto)

    async def update_vehicle(self):
        pass

    async def delete_vehicle(self, vehicle_uuid: Guid):
        return self.core.delete_person(self.session_id, vehicle_uuid)

    # -------------------------Get Claims-------------------------------

    async def get_claim_accepted(self, claim_id: int):
        return self.core.find_visitor_request(self.session_id, claim_id)

    async def get_claims(self, accepted: bool):
        if accepted:
            return self.core.get_accepted_visitor_requests(self.session_id)
        return self.core.get_issued_visitor_requests(self.session_id)

    async def get_claims_in_department(self, department_name: str, date_time_from: datetime, status: ClaimStatus):
        all_org_units = self.core.get_org_units_hierarchy(self.session_id)
        org_unit_id: Guid = ""
        for org in all_org_units:
            if org.NAME == department_name:
                org_unit_id = org.ID
        if not org_unit_id:
            raise ParsecIntegrationError(f"Department with name {department_name} not found")
        return self.core.get_visitor_requests(self.session_id, org_unit_id, date_time_from, **dict(status))

    # ------------------------Post Claims-------------------------------

    async def create_claim(self, dto: VisitorRequest.Create):
        return self.core.create_visitor_request(self.session_id, dto)

    # -----------------------Patch Claim----------------------------------

    async def update_not_approved_claim(self, claim_id: int, dto: VisitorRequest.Update):
        claims_not_approved = self.core.get_issued_visitor_requests(self.session_id)
        for claim in claims_not_approved:
            if claim.NUMBER == claim_id and claim.STATUS == 0:
                if dto.PERSON_INFO:
                    claim.PERSON_INFO = dto.PERSON_INFO
                if dto.PURPOSE:
                    claim.PURPOSE = dto.PURPOSE
                if dto.ADMIT_START:
                    claim.ADMIT_START = dto.ADMIT_START
                if dto.ADMIT_END:
                    claim.ADMIT_END = dto.ADMIT_END
                return self.core.save_visitor_request(self.session_id, claim)
        else:
            raise ParsecIntegrationError(f"Claim with id: {claim_id} not found")

    async def update_approved_claim(self, claim_id: int, dto: VisitorRequest.Update):
        claims_approved = self.core.get_accepted_visitor_requests(self.session_id)
        for claim in claims_approved:
            if claim.NUMBER == claim_id and claim.STATUS == 1:
                if dto.PERSON_INFO:
                    claim.PERSON_INFO = dto.PERSON_INFO
                if dto.PURPOSE:
                    claim.PURPOSE = dto.PURPOSE
                if dto.ADMIT_START:
                    claim.ADMIT_START = dto.ADMIT_START
                if dto.ADMIT_END:
                    claim.ADMIT_END = dto.ADMIT_END
                return self.core.save_visitor_request(self.session_id, claim)
        else:
            raise ParsecIntegrationError(f"Claim with id: {claim_id} not found")

    # ----------------------Approve Claim-----------------------------------

    async def approve_claim(self, claim_id: int, access_group_name: str, privileges: list[int]):
        claims_not_approved = self.core.get_issued_visitor_requests(self.session_id)
        for claim in claims_not_approved:
            if claim.NUMBER == claim_id and claim.STATUS == 0:
                # approve claim
                claim.STATUS = 1
                self.core.save_visitor_request(self.session_id, claim)
                # create pass
                person_edit_session = self.core.open_person_editing_session(self.session_id, claim.PERSON_ID)
                # Добываем расписание, по умолчанию есть Круглосуточное
                schedule = next(i for i in self.core.get_access_schedules(self.session_id)
                                if i.NAME == "Круглосуточное")
                # Создаём RFID
                rfid = hex(randint(900_000_000, 999_999_999))[2:]
                acc_group_id = None
                access_groups = self.core.get_access_groups(self.session_id)
                for group in access_groups:
                    if group.NAME == access_group_name:
                        acc_group_id = group.ID
                if not acc_group_id:
                    # Создаём группу доступа
                    acc_group_id = (self.core.create_access_group(self.session_id,
                                                                  access_group_name,
                                                                  schedule.ID)).Value
                mask = None
                if privileges:
                    # Создаем маску привелегий
                    result = 0
                    for i in privileges:  # Пример прохода 2 - проход при блокировке и 6 - Проход при антипассбеке
                        result += 2 ** i  # Вычисляем
                    mask = bin(result)[2:]
                # Устанавливаем привилегии идентификатору
                self.core.set_identifier_privileges(self.session_id, rfid, mask)
                # Формируем ДТО
                dto = Identifier(CODE=rfid, PERSON_ID=claim.PERSON_ID, IS_PRIMARY=True,
                                 ACCGROUP_ID=acc_group_id, PRIVILEGE_MASK=mask, IDENTIFTYPE=0)
                # Ебемся с изменениями идентификатора (Так как по умолчанию стоит BaseIdentifier)
                object_type = self.core.client.get_type('ns0:Identifier')
                object_wrap = xsd.Element('Identifier', object_type)
                identifier_dto = object_wrap(**dict(dto))
                self.core.add_person_identifier(person_edit_session.Value, identifier_dto)
                self.core.activate_visitor_request(self.session_id, claim.ID, rfid)
                return claim
            if claim.NUMBER == claim_id and claim.STATUS == 1:
                raise ParsecIntegrationError(f"Claim with id: {claim_id} already approved")
        else:
            raise ParsecIntegrationError(f"Claim with id: {claim_id} not found")

    async def close_claim(self, claim_id: int):
        claims_approved = self.core.get_accepted_visitor_requests(self.session_id)
        for claim in claims_approved:
            if claim.NUMBER == claim_id and claim.STATUS == 1:
                return self.core.close_visitor_request(self.session_id, claim.ID)
        else:
            raise ParsecIntegrationError(f"Claim with id: {claim_id} not found")
