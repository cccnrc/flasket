import os
from datetime import datetime
from flask import flash, url_for, redirect, render_template, current_app
from app import db
from app.ticket import bp
from flask_login import current_user, login_required
from app.models import User, Ticket, TicketReply
from app.ticket.forms import TicketForm, TicketReplyForm
from app.ticket.forms import ticket_app, ticket_arg, urgency_choices
from app.ticket.email import send_ticket_email, send_ticket_closure_email, send_ticket_reopen_email

@bp.route('/index')
@login_required
def index():
    return( render_template( 'ticket/index.html' ))

@bp.route('/all')
@login_required
def all():
    tickets = Ticket.query.all()
    return( render_template( 'ticket/all.html',
                ticket_app = dict(ticket_app),
                ticket_arg = dict(ticket_arg),
                urgency_choices = dict(urgency_choices),
                tickets=tickets ))


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    tickets = user.tickets.all()
    ticket_replies = user.ticket_replies.all()
    tickets_followed = user.tickets_followed
    return( render_template( 'ticket/user.html',
                                ticket_app = dict(ticket_app),
                                ticket_arg = dict(ticket_arg),
                                urgency_choices = dict(urgency_choices),
                                user=user,
                                tickets=tickets,
                                ticket_replies=ticket_replies,
                                tickets_followed=tickets_followed
                            ))

@bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            author = current_user,
            urgency = form.urgency.data,
            application = form.application.data,
            argument = form.argument.data,
            title = form.title.data,
            body = form.body.data
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket submitted!', 'success')
        return( redirect( url_for('ticket.ticket_reply', ticket_ID = ticket.id )))
    return( render_template( 'ticket/ticket_submit.html', form=form ))


@bp.route('/ticket_reply/<ticket_ID>', methods=['GET', 'POST'])
@login_required
def ticket_reply(ticket_ID):
    user = User.query.filter_by(username=current_user.username).first_or_404()
    ticket = Ticket.query.filter_by(id=ticket_ID).first_or_404()
    ticket_replies = ticket.ticket_replies.all()
    form = TicketReplyForm()
    if form.validate_on_submit():
        follow = form.follow.data
        body = form.body.data
        if follow:
            ticket.ticket_followers.append(user)
        if body:
            ticket_reply = TicketReply(
                replier = current_user,
                original = ticket,
                body = body
                )
            ticket.last_modify = datetime.utcnow()
            ticket.ticket_followers.append(user)
            send_ticket_email(ticket.author, ticket_reply)
            for single_user in ticket.ticket_followers:
                send_ticket_email(single_user, ticket_reply)
            db.session.add(ticket_reply)
        db.session.commit()
        flash('Ticket updated!', 'success')
        return( redirect( url_for('ticket.ticket_reply', ticket_ID = ticket.id )))
    return( render_template( 'ticket/ticket_reply.html',
                        ticket=ticket,
                        ticket_replies=ticket_replies,
                        ticket_app = dict(ticket_app),
                        ticket_arg = dict(ticket_arg),
                        urgency_choices = dict(urgency_choices),
                        form = form
                        ))

@bp.route('/close/<ticket_ID>')
@login_required
def close(ticket_ID):
    ticket = Ticket.query.filter_by(id=ticket_ID).first_or_404()
    ticket.closed = True
    ticket.closed_on = datetime.utcnow()
    send_ticket_closure_email(ticket.author, ticket)
    for single_user in ticket.ticket_followers:
        send_ticket_closure_email(single_user, ticket)
    db.session.commit()
    return( redirect( url_for('ticket.ticket_reply', ticket_ID = ticket.id )))

@bp.route('/reopen/<ticket_ID>')
@login_required
def reopen(ticket_ID):
    ticket = Ticket.query.filter_by(id=ticket_ID).first_or_404()
    ticket.closed = False
    ticket.last_modify = datetime.utcnow()
    send_ticket_reopen_email(ticket.author, ticket)
    for single_user in ticket.ticket_followers:
        send_ticket_reopen_email(single_user, ticket)
    db.session.commit()
    return( redirect( url_for('ticket.ticket_reply', ticket_ID = ticket.id )))
