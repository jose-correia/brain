from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

# Input Validators
class SearchQuery(BaseModel):
    search: Optional[str] = Field(None, description="Search")


class DateQuery(BaseModel):
    date: Optional[str] = Field(None, description="Query date")


class UrlInput(BaseModel):
    url: Optional[str] = Field(None, description="Url input")


class CreateSquad(BaseModel):
    name: Optional[str] = Field(None, description="Squad name")
    cry: Optional[str] = Field(None, description="Squad cry")


class TagsInput(BaseModel):
    tags: List[str] = Field(None, description="List of tags")


class TagDelete(BaseModel):
    tag: str = Field(None, description="Tag to delete")


class Member(BaseModel):
    ist_id: str = Field(None, description="Member id")


class MemberList(BaseModel):
    members: List[str] = Field(None, description="Member list")


class Invitation(BaseModel):
    id: str = Field(None, description="Invitaion id")


class Invitation_external(BaseModel):
    invitation_id: UUID = Field(None, description="Invitaion with external id")


class CompanyName(BaseModel):
    company: str = Field(None, description="Company name")


class Companylist(BaseModel):
    companies: List[str] = Field(None, description="Company name lsit")


class CompanyChatRoom(BaseModel):
    company: Optional[str] = Field(None, description="Company name")
    member: Optional[str] = Field(None, description="Company user")


class PartnerName(BaseModel):
    name: str = Field(None, description="Partner name")


# Response Validators
class StudentDetail(BaseModel):
    name: str = Field(None, description="Student name")
    photo: str = Field(None, description="Student photo")
    ist_id: str = Field(None, description="Student IST id")
    level: Optional[int] = Field(None, description="Student level")
    total_points: int = Field(None, description="Student total points")
    email: Optional[str] = Field(None, description="Student email")
    daily_points: Optional[int] = Field(None, description="Student daily points")
    squad_points: Optional[int] = Field(None, description="Student squad points")
    linkedin_url: Optional[str] = Field(None, description="Student linkedin_url")
    uploaded_cv: Optional[bool] = Field(None, description="Student uploaded cv")
    companies: Optional[List[str]] = Field(None, description="Student company list")
    tags: Optional[List[str]] = Field(None, description="Student tags list")
    login_dates: Optional[List[datetime]] = Field(
        None, description="Student login dates"
    )
    referral_code: Optional[str] = Field(None, description="Student referral code")


class StudentInfoList(BaseModel):
    list: Dict[str, List[StudentDetail]] = Field(
        None, description="Student information list"
    )


class APIError(BaseModel):
    error: str = Field(None, description="Error")


class Rewards(BaseModel):
    name: Optional[Dict[str, str]] = Field(None, description="Reward name")
    image: Optional[Dict[str, str]] = Field(None, description="Reward image")


class LevelDetail(BaseModel):
    value: int = Field(None, description="Level value")
    end_points: int = Field(None, description="Level end points")
    start_points: int = Field(None, description="Level start points")
    reward: Optional[Dict[str, Rewards]] = Field(None, description="Level value")


class LevelDetailList(BaseModel):
    list: Optional[Dict[str, List[LevelDetail]]] = Field(
        None, description="Student information list"
    )


class SquadMembersDetail(BaseModel):
    name: str = Field(None, description="Squad Member name")
    ist_id: str = Field(None, description="Squad Member ist id")
    level: int = Field(None, description="Squad Member level")
    photo: str = Field(None, description="Squad Member photo")
    squad_points: int = Field(None, description="Squad Member squad points")
    is_captain: bool = Field(None, description="Is this squad member a captain?")


class SquadDetail(BaseModel):
    name: str = Field(None, description="Squad name")
    cry: str = Field(None, description="Squad cry")
    daily_points: int = Field(None, description="Squad daily points")
    total_points: int = Field(None, description="Squad total points")
    image: str = Field(None, description="Squad image")
    members: Dict[str, List[SquadMembersDetail]] = Field(
        None, description="Squad members list"
    )
    captain_ist_id: str = Field(None, description="Squad captains ist id")
    rank: int = Field(None, description="Squad rank")


class SquadDetailList(BaseModel):
    list: Dict[str, List[SquadDetail]] = Field(None, description="Squad list")


class SquadInvitationsSent(BaseModel):
    name: str = Field(None, description="Student name")
    ist_id: str = Field(None, description="Student username")
    level: int = Field(None, description="Student level")
    photo: str = Field(None, description="student photo")
    id: int = Field(None, description="Student id")


class SquadInvitationsSentList(BaseModel):
    list: Dict[str, List[SquadInvitationsSent]] = Field(
        None, description="Squad invitations sent list"
    )


class SquadInvitationsReceived(BaseModel):
    external_id: UUID = Field(None, description="External invitation id")
    squad_name: str = Field(None, description="Squad name")
    squad_cry: str = Field(None, description="Squad cry")
    squad_rank: int = Field(None, description="Squad rank")
    squad_image: str = Field(None, description="Squad image")
    sender_name: str = Field(None, description="Squad invitation sender name")


class SquadInvitationsReceivedList(BaseModel):
    list: Dict[str, List[SquadInvitationsReceived]] = Field(
        None, description="Squad invitations received list"
    )


class SuccessResponse(BaseModel):
    msg: str = Field(None, description="Message")


class Speaker(BaseModel):
    name: str = Field(None, description="Speaker name")
    company: str = Field(None, description="Speaker company")
    company_link: str = Field(None, description="Speaker company link")
    position: str = Field(None, description="Speaker position")
    country: str = Field(None, description="Speaker country")
    bio: str = Field(None, description="Speaker bio")
    linkedin_url: str = Field(None, description="Speaker linkedin url")
    youtube_url: str = Field(None, description="Speaker youtube url")
    website_url: str = Field(None, description="Speaker website url")
    image: str = Field(None, description="Speaker image")
    company_logo: str = Field(None, description="Speaker company logo")


class CompanyDetail(BaseModel):
    name: str = Field(None, description="Company name")
    partnership_tier: str = Field(None, description="Company partnership tier")
    logo: str = Field(None, description="Company logo")
    link: Optional[str] = Field(None, description="Company link")
    business_area: Optional[str] = Field(None, description="Company business area")


class Activity(BaseModel):
    name: str = Field(None, description="Activity name")
    description: str = Field(None, description="Activity description")
    location: str = Field(None, description="Activity location")
    day: str = Field(None, description="Activity day")
    time: str = Field(None, description="Activity time")
    end_time: str = Field(None, description="Activity end time")
    type: int = Field(None, description="Activity type")
    points: int = Field(None, description="Activity points")
    quest: bool = Field(None, description="Activity quest")
    registration_open: bool = Field(None, description="Activity registration open?")
    registration_link: str = Field(None, description="Activity registration link")
    speakers: Dict[str, List[Speaker]] = Field(
        None, description="Activity speaker list"
    )
    moderator: Optional[str] = Field(None, description="Activity moderator")
    companies: Dict[str, List[CompanyDetail]] = Field(
        None, description="Activity company list"
    )
    participated: bool = Field(None, description="Activity participated")
    reward: Dict[str, Rewards] = Field(None, description="Activity reward")
    zoom_url: str = Field(None, description="Activity zoom url")
    interest: bool = Field(None, description="Activity interest")


class ActivityList(BaseModel):
    list: Dict[str, List[Activity]] = Field(None, description="Activity list")


class EventDetail(BaseModel):
    name: str = Field(None, description="Event name")
    description: str = Field(None, description="Event description")


class Event(BaseModel):
    type: Dict[str, List[EventDetail]] = Field(None, description="Event detail list")
    facebook_link: str = Field(None, description="Event facebook link")
    instagram_ling: str = Field(None, description="Event instagram link")


class CompaniesList(BaseModel):
    list: Dict[str, List[CompanyDetail]] = Field(None, description="Companies list")


class CompanyUser(BaseModel):
    name: str = Field(None, description="Company user name")
    post: str = Field(None, description="Company user post")
    user_id: UUID = Field(None, description="Company user id")


class PartnerCompany(BaseModel):
    name: str = Field(None, description="Partner company name")
    business_area: str = Field(None, description="Partner company business area")
    logo: str = Field(None, description="Partner company logo")
    team: Dict[str, List[CompanyUser]] = Field(None, description="Company user list")
    interest: bool = Field(None, description="Partner company user's interest")
    zoom_url: Optional[str] = Field(None, description="Partner company zoom url")


class SquadRewards(BaseModel):
    reward: Dict[str, Rewards] = Field(None, description="Squad reward")
    date: datetime = Field(None, description="Squad reward date")
    winner: bool = Field(None, description="Squad reward if winner")


class SquadRewardsList(BaseModel):
    list: Dict[str, SquadRewards] = Field(None, description="Squad reward list")


class JeecpotRewards(BaseModel):
    first_student_reward: Dict[str, Rewards] = Field(
        None, description="Jeecpot first student reward"
    )
    first_student_winner: bool = Field(None, description="Jeecpot first student winner")
    second_student_reward: Dict[str, Rewards] = Field(
        None, description="Jeecpot second student reward"
    )
    second_student_winner: bool = Field(
        None, description="Jeecpot second student winner"
    )
    third_student_reward: Dict[str, Rewards] = Field(
        None, description="Jeecpot third student reward"
    )
    third_student_winner: bool = Field(None, description="Jeecpot third student winner")
    first_squad_reward: Dict[str, Rewards] = Field(
        None, description="Jeecpot first squad reward"
    )
    first_squad_winner: bool = Field(None, description="Jeecpot first squad winner")
    second_squad_reward: Dict[str, Rewards] = Field(
        None, description="Jeecpot second squad reward"
    )
    second_squad_winner: bool = Field(None, description="Jeecpot second squad winner")
    third_squad_reward: Dict[str, Rewards] = Field(
        None, description="Jeecpot third squad reward"
    )
    third_squad_winner: bool = Field(None, description="Jeecpot third squad winner")
    king_job_fair_reward: Dict[str, Rewards] = Field(
        None, description="Jeecpot King of job fair reward"
    )
    king_job_fair_winner: bool = Field(
        None, description="Jeecpot King of job fair winner"
    )
    king_knowledge_reward: Dict[str, Rewards] = Field(
        None, description="Jeecpot King of knowledge reward"
    )
    king_knowledge_winner: bool = Field(
        None, description="Jeecpot King of knowledge winner"
    )
    king_hacking_reward: Dict[str, Rewards] = Field(
        None, description="Jeecpot King of hacking reward"
    )
    king_hacking_winner: bool = Field(
        None, description="Jeecpot King of hacking winner"
    )
    king_networking_reward: Dict[str, Rewards] = Field(
        None, description="Jeecpot King of networking reward"
    )
    king_networking_winner: bool = Field(
        None, description="Jeecpot King of networking winner"
    )
    cv_platform_raffle_reward: Dict[str, Rewards] = Field(
        None, description="Jeecpot CV platform raffle reward"
    )
    cv_platform_raffle_winner: bool = Field(
        None, description="Jeecpot CV platform raffle winner"
    )
