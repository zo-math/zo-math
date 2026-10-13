"""Load and validate the minimal narration-to-scenes specification."""

import json
import re
from pathlib import Path

ALLOWED_OBJECT_TYPES = {
    "text",
    "equation",
    "axes",
    "function_graph",
    "point",
    "symmetry_axis",
}
ALLOWED_ACTION_TYPES = {"write", "create", "fade_in", "highlight"}
SCENE_ID_PATTERN = re.compile(r"scene_\d{3}\Z")


def validate_scenes(data):
    """Return validation errors; an empty list means the data is valid."""
    errors = []
    if not isinstance(data, dict):
        return ["Gốc scenes phải là một object JSON"]

    scenes = data.get("scenes")
    if not isinstance(scenes, list):
        return ["Trường 'scenes' phải là một danh sách"]
    if not scenes:
        return ["Danh sách 'scenes' không được rỗng"]

    scene_ids = set()
    for scene_index, scene in enumerate(scenes):
        prefix = f"scenes[{scene_index}]"
        if not isinstance(scene, dict):
            errors.append(f"{prefix} phải là một object")
            continue

        scene_id = scene.get("id")
        if not isinstance(scene_id, str) or not SCENE_ID_PATTERN.fullmatch(scene_id):
            errors.append(f"{prefix}.id phải theo dạng scene_NNN")
        elif scene_id in scene_ids:
            errors.append(f"ID scene bị trùng: {scene_id}")
        else:
            scene_ids.add(scene_id)

        for field in ("narration", "visual_intent"):
            value = scene.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{field} không được rỗng")

        objects = scene.get("objects")
        if not isinstance(objects, list):
            errors.append(f"{prefix}.objects phải là một danh sách")
            objects = []

        object_ids = set()
        for object_index, obj in enumerate(objects):
            object_prefix = f"{prefix}.objects[{object_index}]"
            if not isinstance(obj, dict):
                errors.append(f"{object_prefix} phải là một object")
                continue
            object_id = obj.get("id")
            if not isinstance(object_id, str) or not object_id.strip():
                errors.append(f"{object_prefix}.id không được rỗng")
            elif object_id in object_ids:
                errors.append(f"ID object bị trùng trong {prefix}: {object_id}")
            else:
                object_ids.add(object_id)
            object_type = obj.get("type")
            if (
                not isinstance(object_type, str)
                or object_type not in ALLOWED_OBJECT_TYPES
            ):
                errors.append(
                    f"{object_prefix}.type không được hỗ trợ: {object_type!r}"
                )

        actions = scene.get("actions")
        if not isinstance(actions, list):
            errors.append(f"{prefix}.actions phải là một danh sách")
            actions = []

        for action_index, action in enumerate(actions):
            action_prefix = f"{prefix}.actions[{action_index}]"
            if not isinstance(action, dict):
                errors.append(f"{action_prefix} phải là một object")
                continue
            action_type = action.get("type")
            if (
                not isinstance(action_type, str)
                or action_type not in ALLOWED_ACTION_TYPES
            ):
                errors.append(
                    f"{action_prefix}.type không được hỗ trợ: {action_type!r}"
                )
            target = action.get("target")
            if not isinstance(target, str) or not target.strip():
                errors.append(f"{action_prefix}.target không được rỗng")
            elif target not in object_ids:
                errors.append(
                    f"{action_prefix}.target tham chiếu object không tồn tại: {target}"
                )

    return errors


def load_scenes(path):
    """Load JSON from path and raise ValueError if its structure is invalid."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate_scenes(data)
    if errors:
        raise ValueError("Scenes không hợp lệ:\n- " + "\n- ".join(errors))
    return data
