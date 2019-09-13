from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField, RadioField, validators, SubmitField, \
    SelectMultipleField
from dirkules.models import Drive


class CleaningForm(FlaskForm):
    jobname = StringField("Job Name", [validators.required(message="Bitte Feld ausfüllen!"),
                                       validators.none_of('123456789/\\.',
                                                          "Bitte ausschließlich Buchstaben eingeben!"),
                                       validators.Length(max=255, message="Eingabe zu lang")],
                          render_kw={"placeholder": "Dowloads Verzeichnis"})
    path = StringField("Pfad", [validators.required(message="Bitte Feld ausfüllen!"),
                                validators.none_of('\\', "Bitte kein \\"),
                                validators.Length(max=255, message="Eingabe zu lang")],
                       render_kw={"placeholder": "/media/downloads/"})
    active = BooleanField("Sofort aktvieren (Vorsicht!)")
    submit = SubmitField("Job speichern")


class SambaCleaningForm(FlaskForm):
    workgroup = StringField("workgroup", [validators.required(message="Bitte Feld ausfüllen!"),
                                          validators.Regexp('^[a-z]+$', message="Bitte nur Kleinbuchstaben eingeben."),
                                          validators.Length(max=255, message="Eingabe zu lang")],
                            render_kw={"placeholder": "Nichts..."})
    server_string = StringField("server string", [validators.required(message="Bitte Feld ausfüllen!"),
                                                  validators.Regexp('^[a-z]+$',
                                                                    message="Bitte nur Kleinbuchstaben eingeben."),
                                                  validators.Length(max=255, message="Eingabe zu lang")],
                                render_kw={"placeholder": "Nichts..."})


class SambaAddForm(FlaskForm):
    name = StringField("Name der Freigabe", [validators.required(message="Bitte Feld ausfüllen!"),
                                             validators.Length(max=255, message="Eingabe zu lang")],
                       render_kw={"placeholder": "Bilder"})
    writeable = BooleanField("Schreibzugriff")
    recycling = BooleanField("Papierkorb")
    btrfs = BooleanField("BtrFS Optimierungen (Vorsicht!)")
    # additional
    path = SelectField("Pfad", choices=[("Value1", "Label1"), ("Value2", "Label2")])
    user = StringField("Berechtigte Nutzer", [validators.required(message="Bitte Feld ausfüllen!"),
                                              validators.Length(max=255, message="Eingabe zu lang")],
                       render_kw={"placeholder": "sambadaniel"})
    create_mask = IntegerField("Dateimaske", [validators.Optional(),
                                              validators.NumberRange(min=4, max=4,
                                                                     message="Bitte 4 Zahlen eingeben!")],
                               render_kw={"placeholder": "0600"})
    dir_mask = IntegerField("Ordnermaske", [validators.Optional(),
                                            validators.NumberRange(min=4, max=4,
                                                                   message="Bitte 4 Zahlen eingeben!")],
                            render_kw={"placeholder": "0700"})


def get_empty_drives():
    drives = Drive.query.all()
    choices = list()
    for drive in drives:
        label = drive.name + ": " + drive.model + " (" + sizeof_fmt(drive.size) + ")"
        choices.append((drive.name, label))
    return choices


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class CustomMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        if self.data:
            values = list(c[0] for c in self.choices)
            # values_in_data is a list containing all values which are a part of self.data
            # for example: 'sda' is in ['sda,sdb','sdc']
            values_in_data = [value for value in values for d in self.data if value in d]
            if not values_in_data:
                raise ValueError(self.gettext("'%(value)s' is not a valid choice for this field") % dict(value=self.data))


class PoolAddForm(FlaskForm):
    name = StringField("Name", [validators.required(message="Bitte Feld ausfüllen!"),
                                validators.Length(max=255, message="Eingabe zu lang")],
                       render_kw={"placeholder": "whirlpool"})
    raid_config = RadioField("RAID Konfiguration", choices=[(1, "Single"), (2, "RAID0"), (3, "RAID1")],
                             coerce=int)
    drives = CustomMultipleField("Festplatte", choices=get_empty_drives(),
                                 validators=[validators.required(message="Bitte eine Auswahl treffen!")])
    inode_cache = BooleanField("inode_cache")
    space_cache = RadioField("", choices=[(1, "Deaktiviert"), (2, "v1"), (3, "v2")],
                             coerce=int)
    ssd = BooleanField("ssd")
    autodefrag = BooleanField("autodefrag")
    compression = RadioField("", choices=[(1, "Keine"), (2, "zlib"), (3, "lzo")],
                             coerce=int)
    submit = SubmitField("Pool erstellen")
