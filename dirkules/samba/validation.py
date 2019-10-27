from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, validators, SubmitField


class SambaConfigForm(FlaskForm):
    workgroup = StringField("workgroup", [validators.required(message="Bitte Feld ausfüllen!"),
                                          validators.Regexp('^[a-z]+$', message="Bitte nur Kleinbuchstaben eingeben."),
                                          validators.Length(max=255, message="Eingabe zu lang")],
                            render_kw={"placeholder": "Nichts..."})
    server_string = StringField("server string", [validators.required(message="Bitte Feld ausfüllen!"),
                                                  validators.Regexp('^[a-z]+$',
                                                                    message="Bitte nur Kleinbuchstaben eingeben."),
                                                  validators.Length(max=255, message="Eingabe zu lang")],
                                render_kw={"placeholder": "Nichts..."})
    submit = SubmitField("Speichern")


class SambaAddForm(FlaskForm):
    name = StringField("Name der Freigabe", [validators.InputRequired(message="Bitte Feld ausfüllen!"),
                                             validators.Length(max=255, message="Eingabe zu lang")],
                       render_kw={"placeholder": "Bilder"})
    writeable = BooleanField("Schreibzugriff")
    recycling = BooleanField("Papierkorb")
    btrfs = BooleanField("BtrFS Optimierungen (Vorsicht!)")
    path = SelectField("Pfad", validators=[validators.InputRequired(message="Bitte eine Auswahl treffen!")])
    user = StringField("Berechtigte Nutzer", [validators.InputRequired(message="Bitte Feld ausfüllen!"),
                                              validators.Length(max=255, message="Eingabe zu lang")],
                       render_kw={"placeholder": "sambadaniel"})
    create_mask = StringField("Dateimaske", [validators.Optional(),
                                             validators.Regexp('^[0-7]{4}$', message="Dies ist kein gültiger Wert!")],
                              render_kw={"placeholder": "0600"})
    dir_mask = StringField("Ordnermaske", [validators.Optional(),
                                           validators.Regexp('^[0-7]{4}$', message="Dies ist kein gültiger Wert!")],
                           render_kw={"placeholder": "0700"})
    submit = SubmitField("Freigabe hinzufügen")
