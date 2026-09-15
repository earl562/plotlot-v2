from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field

JsonScalar = str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class UnsupportedArcGISHostError(ValueError):
    host: str

    def __str__(self) -> str:
        return f"ArcGIS host is not an approved county publisher: {self.host}"


@dataclass(frozen=True, slots=True)
class ArcGISResponseError(RuntimeError):
    code: int
    message: str
    details: tuple[str, ...]

    def __str__(self) -> str:
        return f"ArcGIS response error {self.code}: {self.message}"


class ArcGISErrorPayload(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    code: int
    message: str
    details: tuple[str, ...] = ()


class ArcGISErrorEnvelope(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    error: ArcGISErrorPayload | None = None


class ArcGISField(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    name: str
    alias: str = ""
    type: str = ""


class ArcGISAdvancedCapabilities(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    supportsPagination: bool = False


class ArcGISMetadata(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    maxRecordCount: int = Field(default=1000, gt=0)
    objectIdField: str | None = None
    objectIdFieldName: str | None = None
    advancedQueryCapabilities: ArcGISAdvancedCapabilities = ArcGISAdvancedCapabilities()
    fields: tuple[ArcGISField, ...] = ()


class ArcGISGeometry(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    x: float | None = None
    y: float | None = None
    rings: tuple[tuple[tuple[float, ...], ...], ...] = ()
    paths: tuple[tuple[tuple[float, ...], ...], ...] = ()


class ArcGISFeature(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    attributes: dict[str, JsonScalar]
    geometry: ArcGISGeometry | None = None


class ArcGISFeatureEnvelope(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    features: tuple[ArcGISFeature, ...] = ()
    exceededTransferLimit: bool = False


@dataclass(frozen=True, slots=True)
class ArcGISQuery:
    layer_url: str
    latitude: float
    longitude: float
    radius_miles: float
    out_fields: tuple[str, ...]
    out_field_tails: tuple[str, ...] = ()
    where: str = "1=1"
    max_records: int = 5000


@dataclass(frozen=True, slots=True)
class ArcGISFeatureResult:
    features: tuple[ArcGISFeature, ...]
    fields: tuple[ArcGISField, ...]
    partial: bool
    notes: tuple[str, ...]
