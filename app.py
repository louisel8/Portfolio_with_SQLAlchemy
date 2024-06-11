from flask import (
    render_template,
    redirect,
    url_for,
    flash,
)
from models import app, db, Project, ProjectForm


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/allprojects")
def all_projects():
    projects = Project.query.all()
    return render_template('allprojects.html', projects=projects)


@app.route('/projects/new', methods=['GET', 'POST'])
def add_new_project():
    form = ProjectForm()
    repeat_project_error = None
    date_format_error = None

    if form.validate_on_submit():
        existing_project = Project.query.filter_by(title=form.title.data).first()
        date_valid = True
        title_valid = True

        try:
            date = form.date.data
        except ValueError:
            date_format_error = 'Invalid data. Please enter a valid date.'
            date_valid = False

        if existing_project:
            repeat_project_error = 'Project title already exists. Please choose a different title.'
            title_valid = False

        if date_valid and title_valid:
            new_project = Project(
                title=form.title.data,
                date=form.date.data,
                description=form.description.data,
                skills=form.skills.data,
                github_link=form.github_link.data
            )
            db.session.add(new_project)
            db.session.commit()
            return redirect(url_for('all_projects'))

    return render_template('addproject.html', form=form, repeat_project_error=repeat_project_error, date_format_error=date_format_error)


@app.route("/projects/<int:id>")
def view_project(id):
    project = Project.query.get_or_404(id)
    return render_template("project.html", project=project)


@app.route("/projects/edit/<int:id>", methods=["GET", "POST"])
def edit_project(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)

    repeat_project_error = None
    date_format_error = None

    if form.validate_on_submit():
        existing_project = Project.query.filter(Project.title == form.title.data, Project.id != id).first()
        date_valid = True
        title_valid = True

        try:
            date = form.date.data
        except ValueError:
            date_format_error = 'Invalid data. Please enter a valid date.'
            date_valid = False

        if existing_project:
            repeat_project_error = 'Project title already exists. Please choose a different title.'
            title_valid = False

        if date_valid and title_valid:
            form.populate_obj(project)
            date = form.date.data
            db.session.commit()
            return redirect(url_for("all_projects"))

    return render_template("editproject.html", form=form, project=project, repeat_project_error=repeat_project_error, date_format_error=date_format_error)


@app.route("/projects/delete/<int:id>", methods=["POST"])
def delete_project(id):
    project = Project.query.get_or_404(id)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Project successfully deleted!', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        db.session.rollback()

    return redirect(url_for("index"))


@app.route("/allprojects")
def about_me():
    return render_template("allprojects.html")


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000, host="127.0.0.1")
