from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from apps.tenancy.models import Workspace, WorkspaceMembership, WorkspaceProfile, LegalEntity, BusinessUnit
from apps.actions.models import ActionItem, ActionComment
from apps.sources.models import ImportBatch

User = get_user_model()

class WorkspaceProfileSerializer(serializers.ModelSerializer):
    source_systems = serializers.ListField(
        child=serializers.ChoiceField(choices=WorkspaceProfile.SourceSystem.choices),
        required=False,
        default=list,
    )
    selected_modules = serializers.ListField(
        child=serializers.ChoiceField(choices=WorkspaceProfile.Module.choices),
        required=True,
        allow_empty=False,
    )
    other_requirements = serializers.CharField(required=False, allow_blank=True, max_length=2000)

    class Meta:
        model = WorkspaceProfile
        fields = [
            "industry", "operating_model", "entity_count_band", "source_systems",
            "selected_modules", "other_requirements", "template_version", "updated_at",
        ]
        read_only_fields = ["template_version", "updated_at"]


class WorkspaceSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    profile = WorkspaceProfileSerializer(read_only=True)

    class Meta:
        model = Workspace
        fields = ["id", "name", "default_currency", "timezone", "status", "created_at", "role", "profile"]
        read_only_fields = ["id", "status", "created_at", "role", "profile"]


class CreateWorkspaceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=160)
    default_currency = serializers.CharField(max_length=3, default="XAF", validators=[RegexValidator(r"^[A-Z]{3}$")])
    timezone = serializers.CharField(max_length=64, default="Africa/Douala")
    profile = WorkspaceProfileSerializer(required=False)

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        user = self.context.get("user")
        if user is None:
            user = self.context["request"].user
        workspace = Workspace.objects.create(owner=user, **validated_data)
        WorkspaceMembership.objects.create(workspace=workspace, user=user, role=WorkspaceMembership.Role.OWNER)
        if profile_data is not None:
            WorkspaceProfile.objects.create(workspace=workspace, **profile_data)
        return workspace

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalEntity
        fields = ["id", "workspace", "parent", "name", "code", "country_code", "functional_currency", "sector", "timezone", "status", "created_at"]
        read_only_fields = ["id", "workspace", "status", "created_at"]
    def validate_parent(self, parent):
        workspace = self.context["workspace"]
        if parent and parent.workspace_id != workspace.id:
            raise serializers.ValidationError("La société mère doit être dans le même workspace.")
        return parent

class BusinessUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = ["id", "entity", "name", "code", "unit_type", "manager", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]
    def validate(self, attrs):
        entity = attrs.get("entity", getattr(self.instance, "entity", None))
        workspace = self.context["workspace"]
        if entity and entity.workspace_id != workspace.id:
            raise serializers.ValidationError({"entity": "Entité hors du workspace actif."})
        manager = attrs.get("manager")
        if manager and not WorkspaceMembership.objects.filter(workspace=workspace, user=manager, is_active=True).exists():
            raise serializers.ValidationError({"manager": "Le responsable doit être membre actif du workspace."})
        return attrs

class ActionCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    class Meta:
        model = ActionComment
        fields = ["id", "author", "author_name", "body", "created_at"]
        read_only_fields = ["id", "author", "created_at"]

class ActionSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.get_full_name", read_only=True)
    assigned_to_name = serializers.CharField(source="assigned_to.get_full_name", read_only=True)
    comments = ActionCommentSerializer(many=True, read_only=True)
    class Meta:
        model = ActionItem
        fields = ["id", "workspace", "entity", "title", "description", "priority", "status", "created_by", "created_by_name", "assigned_to", "assigned_to_name", "due_at", "completed_at", "created_at", "updated_at", "comments"]
        read_only_fields = ["id", "workspace", "created_by", "completed_at", "created_at", "updated_at", "comments"]
    def validate(self, attrs):
        workspace = self.context["workspace"]
        entity = attrs.get("entity", getattr(self.instance, "entity", None))
        assigned_to = attrs.get("assigned_to", getattr(self.instance, "assigned_to", None))
        for item, label in [(entity, "entity"), (assigned_to, "assigned_to")]:
            if item and label == "entity" and item.workspace_id != workspace.id:
                raise serializers.ValidationError({label: "Entité hors du workspace actif."})
            if item and label == "assigned_to" and not WorkspaceMembership.objects.filter(workspace=workspace, user=item, is_active=True).exists():
                raise serializers.ValidationError({label: "Le responsable doit être membre actif du workspace."})
        return attrs

class ImportBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportBatch
        fields = ["id", "workspace", "entity", "original_filename", "sha256", "size_bytes", "detected_mime", "report_type", "period_start", "period_end", "currency", "status", "uploaded_by", "created_at", "mapping", "rows_seen", "rows_staged", "rows_rejected", "validated_at"]
        read_only_fields = ["id", "workspace", "original_filename", "sha256", "size_bytes", "detected_mime", "status", "uploaded_by", "created_at", "mapping", "rows_seen", "rows_staged", "rows_rejected", "validated_at"]
