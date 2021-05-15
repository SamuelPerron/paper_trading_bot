from .. import db
from .constants import DEFAULT_TIME_FORMAT, VARCHAR_TYPE, DATETIME_TYPE, STRING_TYPE


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors


class ModelSerializer:
    model = None
    fields = ()
    custom_fields = ()

    def __init__(self, instance, created=False):
        self.instance = instance
        self.created = created
        self.errors = []

        self._validate_fields()
        self._validate_custom_fields()
        self._compute_fields()

        if created:
            self._create_instance()

    def _validate_fields(self):
        if not len(self.fields) > 0:
            raise ValueError("Specified fields can't be empty.")

        if self.fields != '__all__':
            for field in self.fields:
                if not hasattr(self.model, field):
                    raise ValueError(f"Field `{field}` not in model.")

    def _validate_custom_fields(self):
        for field in self.custom_fields:
            if not hasattr(self, f'get_{field}'):
                raise ValueError(f"Custom field `{field}` has no getter.")

    def _compute_fields(self):
        if self.fields == '__all__':
            self.fields = self.model.get_public_fields()

    def _create_instance(self):
        final_instance = self.model()
        self.is_valid(final_instance)
        
        if len(self.errors) == 0:
            final_instance.save_to_db()
            self.instance = final_instance
        else:
            return self.errors

    def is_valid(self, final_instance):
        for attr in self.instance.keys():
            value = self.instance[attr]
            self._validate_attr(attr, value)

            if hasattr(self, f'set_{attr}'):
                getattr(self, f'set_{attr}')(final_instance, value)
            else:
                setattr(final_instance, attr, value)

    def to_representation(self):
        representation = {
            attr: self._field_to_representation(
                attr, getattr(self.instance, attr)
            ) for attr in self.fields
        }
        representation.update({
            field: getattr(self, f'get_{field}')()
            for field in self.custom_fields
        })

        return representation

    def _field_to_representation(self, attr, value):
        if value is None:
            return None

        attr_type = getattr(self.model, attr).property.columns[0].type

        if str(attr_type) == VARCHAR_TYPE:
            return str(value)

        if str(attr_type) == DATETIME_TYPE:
            return value.strftime(DEFAULT_TIME_FORMAT)

        return value

    def _validate_attr(self, attr, value):
        if hasattr(self, f'valid_{attr}'):
            getattr(self, f'valid_{attr}')(value)
            return
        
        try:
            attr_type = getattr(self.model, attr).property.columns[0].type
        except AttributeError:
            self.errors.append({
                'field': attr,
                'error': f'Model does not have a field named `{attr}`.'
            })
            return
        
        try:
            assert type(value) == attr_type.python_type
        except AssertionError:
            self.errors.append({
                'field': attr, 
                'error': 'Incorrect type.',
            })
            return