from wtforms import Form, StringField, BooleanField, IntegerField, validators


class CleaningForm(Form):
    jobname = StringField("Job Name", [validators.required(message="Bitte Feld ausfüllen!"),
                                       validators.none_of('123456789/\\.',
                                                          "Bitte ausschließlich Buchstaben eingeben!"),
                                       validators.Length(max=255, message="Eingabe zu lang")],
                          render_kw={"placeholder": "Dowloads Verzeichnis"})
    path = StringField("Pfad", [validators.required(message="Bitte Feld ausfüllen!"),
                                validators.none_of('\\', "Bitte kein \\"),
                                validators.Length(max=255, message="Eingabe zu lang")],
                       render_kw={"placeholder": "/media/downloads/"})
    active = BooleanField("Sofort aktvieren (Vorsicht!)", render_kw={"placeholder": "/media/downloads/"})


class samba_cleaning_form(Form):
    workgroup = StringField("workgroup", [validators.required(message="Bitte Feld ausfüllen!"),
                                          validators.Regexp('^[a-z]+$', message="Bitte nur Kleinbuchstaben eingeben."),
                                          validators.Length(max=255, message="Eingabe zu lang")],
                            render_kw={"placeholder": "Nichts..."})
    server_string = StringField("server string", [validators.required(message="Bitte Feld ausfüllen!"),
                                                  validators.Regexp('^[a-z]+$',
                                                                    message="Bitte nur Kleinbuchstaben eingeben."),
                                                  validators.Length(max=255, message="Eingabe zu lang")],
                                render_kw={"placeholder": "Nichts..."})


class SambaAddForm(Form):
    name = StringField("Name der Freigabe", [validators.required(message="Bitte Feld ausfüllen!"),
                                             validators.Length(max=255, message="Eingabe zu lang")],
                       render_kw={"placeholder": "Bilder"})
    writeable = BooleanField("Schreibzugriff")
    recycling = BooleanField("Papierkorb")
    btrfs = BooleanField("BtrFS Optimierungen (Vorsicht!)")
    # additional
    path = StringField("Pfad", [validators.required(message="Bitte Feld ausfüllen!"),
                                validators.Length(max=255, message="Eingabe zu lang")],
                       render_kw={"placeholder": "/media/Bilder"})
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
