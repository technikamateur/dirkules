from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField, RadioField, validators, SubmitField


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
    submit = SubmitField("Speichern")