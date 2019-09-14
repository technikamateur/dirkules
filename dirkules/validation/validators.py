from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField, RadioField, validators, SubmitField
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




class SemanticMultiSelectField(SelectField):
    def pre_validate(self, form):
        if self.choices is not None:
            values_in_data = [value for value, _ in self.choices if value in self.data]
            if not values_in_data:
                raise ValueError(self.gettext('{} is not a valid choice'.format(self.data)))
        else:
            raise ValueError(self.gettext('There are no elements available but this field is required.'))


class ToggleBooleanField(BooleanField):
    pass


class PoolAddForm(FlaskForm):
    name = StringField("Name", [validators.required(message="Bitte Feld ausfüllen!"),
                                validators.Length(max=255, message="Eingabe zu lang")],
                       render_kw={"placeholder": "whirlpool"})
    raid_config = RadioField("RAID Konfiguration", choices=[(1, "Single"), (2, "RAID0"), (3, "RAID1")],
                             coerce=int)
    drives = SemanticMultiSelectField("Festplatte",
                                      validators=[validators.required(message="Bitte eine Auswahl treffen!")])
    inode_cache = BooleanField("inode_cache")
    space_cache = RadioField("", choices=[(1, "Deaktiviert"), (2, "v1"), (3, "v2")],
                             coerce=int)
    ssd = BooleanField("ssd")
    autodefrag = BooleanField("autodefrag")
    compression = RadioField("", choices=[(1, "Keine"), (2, "zlib"), (3, "lzo")],
                             coerce=int)
    okay = ToggleBooleanField("Ich kenne das Risiko und formatiere oben angegebene Laufwerke.",
                              validators=[validators.required(message="Bitte das Risiko akzeptieren.")])
    submit = SubmitField("Pool erstellen")
