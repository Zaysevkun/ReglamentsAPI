from django.contrib.auth.models import Group, User
from django.core.mail import EmailMessage
from rest_framework import serializers

from api.consts import TEXT1_LABEL, TEXT2_LABEL, TEXT3_LABEL, TEXT4_LABEL, TEXT5_LABEL
from api.helpers import send_mail_to_department_users
from api.models import Department, Regulations, AdditionalUserInfo, Revisions, Applications


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'is_regulator')


class UserInfoSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True, source='info.department')
    department_id = serializers.PrimaryKeyRelatedField(
        required=True, source='department', write_only=True,
        queryset=Department.objects.all())
    password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(source='info.phone_number')
    patronymic_name = serializers.CharField(source='info.patronymic_name', required=False)
    is_deleted = serializers.BooleanField(source='info.is_deleted', required=False)
    allow_send_info_emails = serializers.BooleanField(source='info.allow_send_info_emails',
                                                      required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'phone_number', 'department',
                  'department_id', 'first_name', 'patronymic_name', 'last_name', 'is_deleted',
                  'is_superuser', 'allow_send_info_emails')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'patronymic_name': {'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        info = validated_data.pop('info')
        department = validated_data.pop('department')
        info['department_id'] = department.id
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password, **validated_data)
        info = AdditionalUserInfo.objects.create(**info)
        info.user = user
        info.save()
        return User.objects.get(id=user.id)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class DepartmentsUsersSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ('name', 'user', 'status')

    @staticmethod
    def get_user(obj):
        user_info = obj.users.all()
        if user_info:
            return UserInfoSerializer(user_info.first().user).data
        else:
            return {}

    def get_status(self, obj):
        regulations = Regulations.objects.get(id=self.context['regulations_id'])
        user = obj.users.all().first().user
        if user.id in list(regulations.approved.all().values_list('id', flat=True)):
            return "Согласовано"
        if Revisions.objects.filter(regulations_id=regulations.id, created_by=user.id):
            return "Ошибка"
        return "Ожидает согласования"


class RevisionsSerializer(serializers.ModelSerializer):
    created_by = UserInfoSerializer(read_only=True)
    regulations_id = serializers.IntegerField()

    class Meta:
        model = Revisions
        fields = ('id', 'report', 'regulations_id', 'created_by',
                  'regulation_part', 'created_at', 'html_selection',
                  'is_marked_solved', 'secret_id', 'default_text')

    def update(self, instance, validated_data):
        is_marked_solved = validated_data.pop('is_marked_solved', None)
        if is_marked_solved is not None:
            subject = None
            body = None
            to = None
            if is_marked_solved and not instance.is_marked_solved:
                subject = "Ваша правка отмечена как решенная"
                body = "Крутой текст со ссылками"
                to = instance.created_by.email
            if not is_marked_solved and instance.is_marked_solved:
                subject = "Правка переведена обратно в статус не решенная"
                body = "Очень крутой текст со ссылками"
                to = instance.regulations.created_by.email
            if subject and body and to:
                email = EmailMessage(subject=subject, to=[to], body=body)
                email.send()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        created_by = self.context['request'].user
        validated_data['created_by'] = created_by
        revisions = super().create(validated_data)

        if created_by.info.allow_send_info_emails and created_by.email:
            subject = "В созданный Вами регламент добавлена правка."
            body = ('В созданный Вами регламент добавлена правка. Тут должна быть ссылка на правку,'
                    'Кирилл, не забудь!!')
            created_by = revisions.regulations.created_by
            email = EmailMessage(subject, to=[created_by.email]
                if created_by.info.allow_send_info_emails else [], body=body)
            email.send()
        return revisions


class Text1Serializer(serializers.ModelSerializer):
    label = TEXT1_LABEL
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('label', 'text', 'comments')

    @staticmethod
    def get_text(obj):
        return obj.text1

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='text1'),
                                   many=True).data


class Text2Serializer(serializers.ModelSerializer):
    label = TEXT2_LABEL
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('label', 'text', 'comments')

    @staticmethod
    def get_text(obj):
        return obj.text2

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='text2'),
                                   many=True).data


class Text3Serializer(serializers.ModelSerializer):
    label = TEXT3_LABEL
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('label', 'text', 'comments')

    @staticmethod
    def get_text(obj):
        return obj.text3

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='text3'),
                                   many=True).data


class Text4Serializer(serializers.ModelSerializer):
    label = TEXT4_LABEL
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('label', 'text', 'comments')

    @staticmethod
    def get_text(obj):
        return obj.text4

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='text4'),
                                   many=True).data


class Text5Serializer(serializers.ModelSerializer):
    label = TEXT5_LABEL
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('label', 'text', 'comments')

    @staticmethod
    def get_text(obj):
        return obj.text5

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='text5'),
                                   many=True).data


class LabelSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('text', 'comments')

    @staticmethod
    def get_comments(obj):
        return RevisionsSerializer(obj.revisions.all().filter(regulation_part='label'),
                                   many=True).data

    @staticmethod
    def get_text(obj):
        return obj.label


class PartsSerializer(serializers.ModelSerializer):
    text1 = Text1Serializer(source='*')
    text2 = Text2Serializer(source='*')
    text3 = Text3Serializer(source='*')
    text4 = Text4Serializer(source='*')
    text5 = Text5Serializer(source='*')
    label = LabelSerializer(source='*')

    class Meta:
        model = Regulations
        fields = ('text1', 'text2', 'text3', 'text4', 'text5', 'label')


class RegulationsSerializer(serializers.ModelSerializer):
    approved = UserInfoSerializer(many=True, read_only=True)
    approver_id = serializers.IntegerField(write_only=True, required=False)
    do_approve = serializers.BooleanField(write_only=True)
    created_by = UserInfoSerializer(read_only=True)
    updated_by = UserInfoSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    parts = PartsSerializer(read_only=True, source='*')
    departments_users = serializers.SerializerMethodField()
    application_urls = serializers.SerializerMethodField()

    class Meta:
        model = Regulations
        fields = ('id', 'name', 'version', 'version_history_id', 'departments',
                  'created_at', 'updated_at', 'status', 'created_by', 'updated_by',
                  'approved', 'departments_users', 'parts', 'do_approve',
                  'text1', 'text2', 'text3', 'text4', 'text5', 'label',
                  'approver_id', 'application_urls')
        extra_kwargs = {
            'version': {'read_only': True},
            'version_history_id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'departments': {'read_only': True},
            'text1': {'write_only': True},
            'text2': {'write_only': True},
            'text3': {'write_only': True},
            'text4': {'write_only': True},
            'text5': {'write_only': True},
            'label': {'write_only': True}
        }

    @staticmethod
    def get_departments_users(obj):
        return DepartmentsUsersSerializer(obj.departments.all(), many=True,
                                          context={'regulations_id': obj.id}).data

    def get_application_urls(self, obj):
        request = self.context.get('request')
        applications = obj.applications.all()
        application_urls = [request.build_absolute_uri(application.app_file.url) for application in
                            applications]
        return application_urls

    def save(self, **kwargs):
        approver_id = self.validated_data.pop('approver_id', False)
        do_approve = self.validated_data.pop('do_approve', False)
        regulations = super().save(**kwargs)
        if do_approve:
            departments = Department.objects.filter(is_regulator=True)
            send_mail_to_department_users(departments)
            regulations.departments.add(*list(departments.values_list('id', flat=True)))
        if approver_id:
            regulations.approved.add(approver_id)
        return Regulations.objects.get(id=regulations.id)

    def update(self, instance, validated_data):
        is_new_version = bool({'text1', 'text2', 'text3', 'text4', 'text5', 'load'}
                              .intersection(set(validated_data.keys())))
        if is_new_version and instance.version_history_id:
            regulations_history = Regulations.objects.filter(
                version_history_id=instance.version_history_id
            ).order_by('-version')
            instance = regulations_history.first()
        regulations = super().update(instance, validated_data)
        if is_new_version:
            past_regulations = Regulations.objects.create(
                name=instance.name,
                label=instance.label,
                text1=instance.text1,
                text2=instance.text2,
                text3=instance.text3,
                text4=instance.text4,
                text5=instance.text5,
                created_by=instance.created_by,
                updated_by=instance.updated_by
            )
            if instance.version_history_id and instance.version:
                past_regulations.version_history_id = instance.version_history_id
                past_regulations.version = instance.version
            else:
                past_regulations.identify_version(instance.version_history_id, instance.version)
            updated_at = past_regulations.created_at
            past_regulations.created_at = instance.created_at
            past_regulations.updated_at = updated_at
            past_regulations.save()
            regulations.identify_version(past_regulations.version_history_id,
                                         past_regulations.version)
        regulations.updated_by = self.context['request'].user
        regulations.save()

        return Regulations.objects.get(id=regulations.id)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applications
        fields = ('id', 'app_file', 'regulations')
