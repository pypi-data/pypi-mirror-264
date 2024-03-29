# Copyright (c) 2022, INRIA
# Copyright (c) 2022, University of Lille
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging
from typing import Literal, Callable

from powerapi.actor import Actor, State
from powerapi.dispatcher.handlers import FormulaDispatcherReportHandler, DispatcherPoisonPillMessageHandler
from powerapi.dispatcher.route_table import RouteTable
from powerapi.exception import PowerAPIException
from powerapi.handler import StartHandler
from powerapi.report import Report
from powerapi.message import PoisonPillMessage, StartMessage
from powerapi.utils import Tree


class NoPrimaryDispatchRuleRuleException(PowerAPIException):
    """
    Exception raised when user want to get the primary dispatch_rule rule on a
    formula dispatcher that doesn't have one
    """


class PrimaryDispatchRuleRuleAlreadyDefinedException(PowerAPIException):
    """
    Exception raised when user want to add a primary dispatch_rule rule on a
    formula dispatcher that already have one
    """


class DispatcherState(State):
    """
    DispatcherState class herited from State.

    State that encapsulate formula's dicionary and tree

    :attr:`formula_dict
    <powerapi.dispatcher.dispatcher_actor.DispatcherState.formula_dict>`
    :attr:`formula_tree
    <powerapi.dispatcher.dispatcher_actor.DispatcherState.formula_tree>`
    :attr:`formula_factory
    <powerapi.dispatcher.dispatcher_actor.DispatcherState.formula_factory>`
    """

    def __init__(self, actor, pushers, route_table):
        """
        :param actor: Dispatcher actor instance
        :param pushers: List of pushers
        :param route_table: Route table to use for reports
        """
        super().__init__(actor)

        self.formula_dict = {}
        self.formula_tree = Tree()

        self.pushers = pushers
        self.route_table = route_table

    def add_formula(self, formula_id):
        """
        Create a formula corresponding to the given formula id and add it in memory.
        :param tuple formula_id: Define the key corresponding to a specific Formula
        """
        formula = self.actor.formula_init_function(name=str((self.actor.name,) + formula_id), pushers=self.pushers)
        self.supervisor.launch_actor(formula, start_message=False)

        self.formula_dict[formula_id] = formula
        self.formula_tree.add(list(formula_id), formula)

    def get_direct_formula(self, formula_id):
        """
        Get the formula corresponding to the given formula id
        or create and return it if its didn't exist

        :param tuple formula_id: Key corresponding to a Formula
        :return: a Formula
        :rtype: Formula or None
        """
        if formula_id not in self.formula_dict:
            self.add_formula(formula_id)
        return self.formula_dict[formula_id]

    def get_corresponding_formula(self, formula_id):
        """
        Get the Formulas which have id match with the given formula_id

        :param tuple formula_id: Key corresponding to a Formula
        :return: All Formulas that match with the key
        :rtype: list(Formula)
        """
        return self.formula_tree.get(formula_id)


class DispatcherActor(Actor):
    """
    Dispatcher Actor.
    """

    def __init__(self, name: str, formula_init_function: Callable, pushers: [], route_table: RouteTable,
                 level_logger: Literal = logging.WARNING, timeout=None):
        """
        :param str name: Actor name
        :param func formula_init_function: Function for creating Formula
        :param route_table: initialized route table of the DispatcherActor
        :param int level_logger: Define the level of the logger
        :param bool timeout: Define the time in millisecond to wait for a message before run timeout_handler
        """
        Actor.__init__(self, name, level_logger, timeout)

        # (func): Function for creating Formula
        self.formula_init_function = formula_init_function

        # (powerapi.DispatcherState): Actor state
        self.state = DispatcherState(self, pushers, route_table)

    def setup(self):
        """
        Setup Dispatcher actor report handlers.
        """
        super().setup()

        if self.state.route_table.primary_dispatch_rule is None:
            raise NoPrimaryDispatchRuleRuleException()

        self.add_handler(Report, FormulaDispatcherReportHandler(self.state))
        self.add_handler(PoisonPillMessage, DispatcherPoisonPillMessageHandler(self.state))
        self.add_handler(StartMessage, StartHandler(self.state))
