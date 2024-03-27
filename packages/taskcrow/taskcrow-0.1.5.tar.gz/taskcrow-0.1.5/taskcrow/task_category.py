from enum import Enum, auto


class TaskCategory(Enum):
  GRID = (auto(), 'Grid단위 작업 카테고리')

  def __init__(self, code:str, description:str):
    # 초기화 메소드에서는 각 상태에 대한 코드와 설명을 인스턴스 변수로 저장합니다.
    self.code = code
    self.description = description

  def __str__(self):
    # 멤버를 문자열로 변환할 때, 멤버의 이름을 반환합니다.
    # 이는 로깅이나 사용자 인터페이스에서의 표시를 용이하게 합니다.
    return self.name

  @staticmethod
  def get_status_by_code(code):
    # 주어진 코드에 해당하는 상태를 찾아 반환합니다.
    # 해당하는 상태가 없을 경우 None을 반환합니다.
    for status in TaskCategory:
        if status.code == code:
            return status
    return None

  @classmethod
  def list_all_statuses(cls):
    # 클래스 메소드를 사용하여, Enum에 정의된 모든 상태의 이름을 리스트로 반환합니다.
    # 이는 상태의 전체 목록을 얻고자 할 때 유용합니다.
    return list(map(lambda c: c.name, cls))


if __name__ == '__main__':
  # Enum 클래스의 확장된 기능을 시연하기 위한 코드를 출력
  print(TaskCategory.READY) # 멤버를 문자열로 변환
  print(TaskCategory.get_status_by_code(2))  # 코드로부터 상태 검색
  print(TaskCategory.list_all_statuses())  # 모든 상태 목록 출력
