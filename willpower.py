from datetime import datetime, timedelta

file_path = "willpower.json"

class Willpower:
    willpower: int
    timestamp: datetime # UTC time, resolution to minute
    file_path: str
    def __init__(self, file_path: str):
        try:
            json_file = open(file_path, 'r')
            self.file_path = file_path
            self.willpower = json_file['willpower']
            timestamp = json_file['timestamp']
            self.timestamp = datetime(year=timestamp['year'], month=timestamp['month'], day=timestamp['day'], hour=timestamp['hour'], minute=timestamp['minute'], tzinfo=datetime.utcnow().tzinfo)
            json_file.close()
        except:
            print("Cannot Open "+file_path+"!")
            exit()
    def datetime_resolution_to_minute(timestamp: datetime) -> datetime:
        return datetime(year=timestamp.year, month=timestamp.month, day=timestamp.day, hour=timestamp.hour, minute=timestamp.minute, tzinfo=timestamp.tzinfo)
    def record(self):
        pass
    def refresh(self):
        now: datetime = self.datetime_resolution_to_minute(datetime.utcnow())
        if now != self.timestamp:
            self.willpower += (now - self.timestamp) / timedelta(minutes=1)
            self.timestamp = now
    def value(self) -> int:
        self.refresh()
        return self.willpower



