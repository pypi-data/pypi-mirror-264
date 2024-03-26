#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from typing import Any, cast, Dict, List, Optional

import trafaret as t

from datarobot.insights.base import BaseInsight


class ShapImpact(BaseInsight):
    """
    Shap Impact Insight
    """

    INSIGHT_NAME = "shapImpact"
    INSIGHT_DATA = {
        "shap_impacts": t.List(t.List(t.Or(t.Int(), t.Float()))),
        "base_value": t.List(t.Float()),
        "capping": t.Or(
            t.Null(),
            t.Dict(
                {
                    t.Key("right"): t.Or(t.String(), t.Float(), t.Null()),
                    t.Key("left"): t.Or(t.String(), t.Float(), t.Null()),
                }
            ),
        ),
        "link": t.Or(t.String(), t.Null()),
        "row_count": t.Int(),
    }

    @property
    def shap_impacts(self) -> List[List[Any]]:
        """SHAP impact values

        Returns
        -------
        shap impacts
            A list of the SHAP impact values
        """
        return cast(List[List[Any]], self.data["shap_impacts"])

    @property
    def base_value(self) -> List[float]:
        """A list of base prediction values"""
        return cast(List[float], self.data["base_value"])

    @property
    def capping(self) -> Optional[Dict[str, Any]]:
        """Capping for the models in the blender"""
        return cast(Optional[Dict[str, Any]], self.data.get("capping"))

    @property
    def link(self) -> Optional[str]:
        """Shared link function of the models in the blender"""
        return cast(Optional[str], self.data.get("link"))

    @property
    def row_count(self) -> int:
        """Number of SHAP impact rows"""
        return cast(int, self.data["row_count"])
