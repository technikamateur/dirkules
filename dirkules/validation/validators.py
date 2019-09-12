from wtforms import StringField, BooleanField, IntegerField, SelectField, validators, RadioField
from flask_wtf import FlaskForm


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


class PoolAddForm(FlaskForm):
    raid_selection = RadioField("RAID Auswahl", choices=[(1, "Single"), (2, "RAID1")],
                                validators=[validators.required(message="Bitte eine Auswahl treffen!")])
