from wtforms import Form, StringField, BooleanField, validators


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
                                     validators.Regexp('^[a-z]+$', message="Bitte nur Kleinbuchstaben eingeben."),
                                     validators.Length(max=255, message="Eingabe zu lang")],
                            render_kw={"placeholder": "Nichts..."})

class SambaAddForm(Form):
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