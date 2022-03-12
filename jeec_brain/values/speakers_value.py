from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.handlers.speakers_handler import SpeakersHandler


class SpeakersValue(ValueComposite):
    def __init__(self, speakers):
        super(SpeakersValue, self).initialize({})
        speakers_array = []
        for speaker in speakers:
            speaker_value = {
                "name": speaker.name,
                "company": speaker.company,
                "company_link": speaker.company_link,
                "position": speaker.position,
                "country": speaker.country,
                "bio": speaker.bio,
                "linkedin_url": speaker.linkedin_url,
                "youtube_url": speaker.youtube_url,
                "website_url": speaker.website_url,
                "image": SpeakersHandler.find_image(speaker.name),
                "company_logo": SpeakersHandler.find_company_logo(speaker.company),
            }
            speakers_array.append(speaker_value)
        self.serialize_with(data=speakers_array)
