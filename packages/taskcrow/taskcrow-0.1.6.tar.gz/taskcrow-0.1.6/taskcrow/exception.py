class DataNotInsertedError(Exception):
  """ 데이터가 데이터베이스에 아직 삽입되지 않았을 때 발생하는 예외"""

  def __init__(self, message="Data has not been inserted into the database yet"):
    self.message = message
    super().__init__(self.message)
