# A mapper that transforms a data row into the proper format
class Mapper(object):

    NAME_COLNAME = "name"
    ID_COLNAME = "id"
    WEEKDAY_COLNAME = "weekday"
    OPENS_AT_COLNAME = "opens_at"
    CLOSES_AT_COLNAME = "closes_at"
    ADD_DAY_COLNAME = "add_day"
    ADD_HOURS_COLNAME = "add_hours"

    def __init__(
        self, name = None, id = None, weekday = None,
        opens_at = None, closes_at = None, add_day = None,
        add_hours = None,
    ):
        self.name = name
        self.id = id
        self.weekday = weekday
        self.opens_at = opens_at
        self.closes_at = closes_at
        self.add_day = add_day
        self.add_hours = add_hours

    def to_dict(self):
        return {
            self.NAME_COLNAME: self.name,
            self.ID_COLNAME: self.id,
            self.WEEKDAY_COLNAME: self.weekday,
            self.OPENS_AT_COLNAME: self.opens_at,
            self.CLOSES_AT_COLNAME: self.closes_at,
            self.ADD_DAY_COLNAME: self.add_day,
            self.ADD_HOURS_COLNAME: self.add_hours,
        }

    @classmethod
    def csv_header(cls):
        return [
            cls.NAME_COLNAME,
            cls.ID_COLNAME,
            cls.WEEKDAY_COLNAME,
            cls.OPENS_AT_COLNAME,
            cls.CLOSES_AT_COLNAME,
            cls.ADD_DAY_COLNAME,
            cls.ADD_HOURS_COLNAME,
        ]
    
    def to_csv_row(self):
        return [self.name, self.id, self.weekday, self.opens_at, self.closes_at, self.add_day, self.add_hours]